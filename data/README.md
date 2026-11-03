# Local ingestion output

This folder starts with no data. A future ingestion step can publish its
normalized export as `documents.jsonl`; the server only reads that export.
The [repo guide](../README.md#data-contract) explains the record fields.

Use `--data` to point to an export elsewhere. Paths supplied through that option
can contain private data; the server never needs the export committed to Git.
`.gitignore` keeps this folder's contents off Git except for this guide.

Publish updates by writing a complete temporary file and renaming it over the
old export. The next tool call rereads the file. A malformed export returns a
tool error; this adapter does not retain the previous version as a fallback.

The tests create and clean up their own temporary exports outside this folder.
Nothing needs to be added here to run the connection checks.
