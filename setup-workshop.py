"""Prepare the workshop's existing code and report what was actually verified.

A local coding agent can run this file, or an attendee can use the fallback:
    uv run python setup-workshop.py
The script installs locked dependencies, runs checks, and rebuilds the generated
page export. It does not connect an agent to the search tools or sign in.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_step(uv: str, label: str, arguments: list[str]) -> str:
    """Run a fixed project command and retain useful diagnostics on failure."""
    print(f"Checking: {label}", flush=True)
    # An argument list works with spaces in paths and avoids shell interpolation.
    # Capturing routine logs keeps the attendee report short; failures show detail.
    result = subprocess.run([uv, *arguments], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        print(f"NEEDS ATTENTION: {label}", file=sys.stderr)
        print("\n".join((result.stdout + "\n" + result.stderr).splitlines()[-25:]), file=sys.stderr)
        print("Ask your setup agent or a presenter to inspect this step.", file=sys.stderr)
        raise SystemExit(result.returncode)
    print(f"  PASS: {label}", flush=True)
    return result.stdout


def main():
    """Verify the local foundation; leave actual client/answer checks explicit."""
    uv = shutil.which("uv")
    if uv is None:
        raise SystemExit("uv is missing. Complete the install prework or ask a presenter for help.")
    print("Preparing the existing RAG-Symposium project.")
    print("This rebuilds data/documents.jsonl from the committed corpus in page mode.")
    run_step(uv, "locked dependencies", ["sync", "--locked"])
    run_step(uv, "project tests", ["run", "--locked", "python", "-m", "unittest", "discover", "-s", "tests", "-v"])
    run_step(uv, "local-process MCP tools", ["run", "--locked", "python", "tests/mcp_smoke.py"])
    run_step(uv, "page ingestion", ["run", "--locked", "rag-ingest", "--mode", "page"])
    # Read through the real adapter, rather than treating an ingestion exit code
    # as proof that the exported records are usable by the server.
    probe = '''
import json
from pathlib import Path
from rag_symposium.store import RecordStore
store = RecordStore(Path("data/documents.jsonl"))
records = store.records()
if not records:
    raise SystemExit("The export contains no records")
record = store.get(records[0]["id"], max_chars=200)
print(json.dumps({"count": len(records), "example_id": record["id"], "source": record["source"]}))
'''
    data = json.loads(run_step(uv, "readable source-linked export", ["run", "--locked", "python", "-c", probe]))
    print("\nWorkshop checkpoints")
    print(f"1. DATA LOADED: verified {data['count']} records; example {data['example_id']}")
    print("2. TOOLS CONNECTED: pending actual chatbot connection; local protocol checks passed")
    print("3. ANSWER SUPPORTED: pending a real chatbot tool call and source check")
    print("Next: follow the Setup steps in AGENTS.md to connect your agent to the search tools.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130)
