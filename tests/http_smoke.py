"""Exercise the HTTP endpoint from an MCP client and simulate browser headers.

The process, port, export and logs belong only to this test. CORS preflight and
Host/Origin checks are verified over real HTTP. This does not open a browser or
verify a particular chatbot website's MCP support or local-network permissions.
Run directly with `uv run python tests/http_smoke.py`.
"""
import asyncio
import json
import socket
import sys
import tempfile
from pathlib import Path

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    """Launch HTTP, check access boundaries, then discover and call the tools."""
    # Let the OS select a free test port rather than taking the workshop's port.
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    url = f"http://127.0.0.1:{port}/mcp"
    origin = "https://client.example"
    with tempfile.TemporaryDirectory(prefix="rag-http-check-") as folder:
        path = Path(folder) / "records.jsonl"
        log_path = Path(folder) / "server.log"
        # Capture logs so startup failures have a useful explanation. Keep stdout
        # separate: HTTP tools use HTTP, not the process's standard output.
        with log_path.open("w+") as log:
            process = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "rag_symposium.server", "--transport", "http",
                "--port", str(port), "--data", str(path), "--allow-origin", origin,
                stdout=asyncio.subprocess.DEVNULL, stderr=log)
            try:
                async with httpx.AsyncClient(timeout=2) as browser:
                    # Wait for readiness instead of assuming a fixed startup time.
                    # Any HTTP response proves the listener is up; GET need not
                    # be a valid MCP call for this readiness probe.
                    for _ in range(100):
                        if process.returncode is not None:
                            raise RuntimeError("Server exited: " + log_path.read_text())
                        try:
                            await browser.get(url)
                            break
                        except httpx.ConnectError:
                            await asyncio.sleep(0.1)
                    else:
                        raise RuntimeError("Server did not start: " + log_path.read_text())
                    # Browsers may send OPTIONS before a cross-origin POST. The
                    # allowed origin gets CORS headers; an unrelated one must not.
                    response = await browser.options(url, headers={"Origin": origin,
                        "Access-Control-Request-Method": "POST",
                        "Access-Control-Request-Headers": "Content-Type,MCP-Protocol-Version"})
                    assert response.status_code == 200
                    assert response.headers["access-control-allow-origin"] == origin
                    response = await browser.options(url, headers={"Origin": "https://untrusted.example",
                        "Access-Control-Request-Method": "POST"})
                    assert response.status_code == 400
                    # Also test actual request rejection. Missing CORS response
                    # headers alone would not stop a server from processing a call.
                    response = await browser.post(url, json={}, headers={"Origin": "https://untrusted.example"})
                    assert response.status_code == 403
                    response = await browser.post(url, json={}, headers={"Host": "untrusted.example"})
                    assert response.status_code in {400, 403, 421}

                # Send the allowed Origin on the full MCP handshake/tool calls,
                # not just the preflight. This tests the same tool registry as stdio.
                async with httpx.AsyncClient(headers={"Origin": origin}) as client:
                    async with streamable_http_client(url, http_client=client) as (read, write, _):
                        async with ClientSession(read, write) as session:
                            await session.initialize()
                            tools = (await session.list_tools()).tools
                            assert {t.name for t in tools} == {"data_status", "search_documents", "get_document"}
                            assert all(t.annotations.readOnlyHint for t in tools)

                            async def call(name, args):
                                """Assert protocol success and unpack the tool's JSON result."""
                                result = await session.call_tool(name, args)
                                assert not result.isError, result.content
                                return json.loads(result.content[0].text)

                            assert (await call("data_status", {}))["record_count"] == 0
                            assert not path.exists()
                            text = "alpha beta " * 100
                            path.write_text(json.dumps({"id": "check-1", "title": "Temporary record",
                                "text": text, "source": "temporary-test-source"}), encoding="utf-8")
                            original = path.read_bytes()
                            match = (await call("search_documents", {"query": "alpha"}))["matches"][0]
                            assert match["citation"] == "[check-1]"
                            # Read every slice to verify pagination over HTTP too.
                            parts, offset = [], 0
                            while offset is not None:
                                record = await call("get_document", {"document_id": match["id"],
                                                                      "offset": offset, "max_chars": 400})
                                parts.append(record["text"])
                                offset = record["next_offset"]
                            assert "".join(parts) == text
                            assert path.read_bytes() == original
                            assert (await session.call_tool("get_document", {"document_id": "missing"})).isError
            finally:
                # Always stop the child, including when an assertion fails, so
                # running the check never leaves a background listener behind.
                if process.returncode is None:
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), timeout=5)
                    except asyncio.TimeoutError:
                        process.kill()
                        await process.wait()
    print("PASS: HTTP MCP handshake, all tools, live data, pagination, CORS and Host/Origin restrictions")


if __name__ == "__main__":
    asyncio.run(main())
