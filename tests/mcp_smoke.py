"""Play the role of a chatbot's MCP client against a real stdio subprocess.

Unlike the unit tests, this checks discovery, schema handling and tool results
over the protocol. It uses no language model, chatbot account or bundled data.
Run directly with `uv run python tests/mcp_smoke.py`; extra arguments go to the
server, so `uv run python tests/mcp_smoke.py --search bm25` checks the other mode.
"""
import asyncio
import json
import sys
import tempfile
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Connect empty, publish temporary text, read it, then verify error behavior."""
    with tempfile.TemporaryDirectory(prefix="rag-mcp-check-") as folder:
        path = Path(folder) / "records.jsonl"
        # Use this test's interpreter so the subprocess has the same installed
        # dependencies. The async context managers close the session/process.
        params = StdioServerParameters(command=sys.executable,
            args=["-m", "rag_symposium.server", "--data", str(path), *sys.argv[1:]])
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                # The handshake comes before discovery or calls. A real chatbot
                # client performs these same protocol steps for the attendee.
                await session.initialize()
                tools = (await session.list_tools()).tools
                assert {t.name for t in tools} == {"data_status", "search_documents", "get_document"}
                assert all(t.annotations.readOnlyHint for t in tools)

                async def call(name, args):
                    """Check success, then decode the SDK's text form of the result."""
                    result = await session.call_tool(name, args)
                    assert not result.isError, result.content
                    return json.loads(result.content[0].text)

                assert (await call("data_status", {}))["record_count"] == 0
                assert (await call("search_documents", {"query": "alpha"}))["matches"] == []
                assert not path.exists()
                # Publish while the process remains connected: the next call
                # should see the export without a restart or a watcher process.
                text = "alpha beta " * 100
                record = {"id": "check-1", "title": "Temporary record", "text": text,
                          "source": "temporary-test-source", "metadata": {"page": 1}}
                path.write_text(json.dumps(record) + "\n", encoding="utf-8")
                original = path.read_bytes()  # Compare later to prove reads did not write.
                assert (await call("data_status", {}))["record_count"] == 1
                match = (await call("search_documents", {"query": "alpha"}))["matches"][0]
                assert match["citation"] == "[check-1]"
                assert match["source"] == "temporary-test-source"
                # A small read window forces pagination. Reassembly detects gaps
                # or overlaps in offsets, not just a plausible-looking excerpt.
                parts, offset = [], 0
                while offset is not None:
                    document = await call("get_document", {"document_id": match["id"],
                                                            "offset": offset, "max_chars": 200})
                    parts.append(document["text"])
                    offset = document["next_offset"]
                assert "".join(parts) == text
                assert path.read_bytes() == original
                # Invalid requests should be MCP tool errors, not process exits.
                for name, args in (("get_document", {"document_id": "/etc/passwd"}),
                                   ("search_documents", {"query": "alpha", "limit": 0})):
                    assert (await session.call_tool(name, args)).isError
                path.write_text("broken JSON", encoding="utf-8")
                assert (await session.call_tool("search_documents", {"query": "alpha"})).isError
                path.unlink()
                assert not (await call("data_status", {}))["data_available"]
    print("PASS: tool discovery, empty startup, live data, citations, pagination, read-only access and errors")


if __name__ == "__main__":
    asyncio.run(main())
