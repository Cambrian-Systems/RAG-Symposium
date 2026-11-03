"""Convenience launcher: start the existing server in local HTTP mode.

Run `uv run python start-local.py` from the repo. This helper adds no new tools:
it delegates to the rag-symposium command defined in pyproject.toml. Extra
arguments, such as --port and --data, are forwarded to that command unchanged.
"""
import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    try:
        # Use the script's own directory so the server finds this project even
        # when the launcher is called by absolute path from another directory.
        # --locked keeps dependency versions aligned with the workshop lockfile.
        # Pass an argument list, not a shell string, so paths with spaces work.
        raise SystemExit(subprocess.call([
            "uv", "run", "--directory", str(Path(__file__).resolve().parent),
            "--locked", "rag-symposium", "--transport", "http", *sys.argv[1:]
        ]))
    except FileNotFoundError:
        raise SystemExit("Install uv first: https://docs.astral.sh/uv/")
    except KeyboardInterrupt:
        # Ctrl+C is the normal way to stop the foreground launcher/server.
        raise SystemExit(130)
