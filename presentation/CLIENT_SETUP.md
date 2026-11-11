# Client connections and presenter preflight

Reviewed November 6, 2026. Present with ChatGPT; retain the same three MCP tools
for compatible alternatives. Provider/model choice and MCP client capability are
separate: a Gemini model used in Gemini CLI is not the same client as Gemini's
consumer website. Do not promise the same setup works across every website,
subscription or organization policy.

## Setup agent versus question-answering client

The local coding agent follows [AGENT_SETUP.md](AGENT_SETUP.md), runs the prepared
setup script and helps configure a client. The question-answering client uses the
three MCP tools to retrieve evidence and generate an answer. They can be different
applications; account names alone do not establish local command access.

Use the agent for environment diagnostics and the existing launcher/configuration.
The attendee completes sign-ins and permission choices. Local setup checks must
not be reported as proof that the chosen client is connected.

## The connection routes

| Client surface | Route to rehearse | Status for this repo |
| --- | --- | --- |
| ChatGPT web custom MCP connection | Local HTTP server through Secure MCP Tunnel, or a separately prepared authenticated remote endpoint | Official route documented; presenter account not yet tested |
| Claude Desktop local MCP configuration | Stdio command/arguments from `mcp.example.json` | Local mechanism documented; this client not yet tested here |
| Gemini CLI | Configured stdio command, or its HTTP MCP transport | Official mechanisms documented; this client not yet tested here |
| Other MCP clients | Check supported transport and network location, then discover the three tools | Validate individually |

Our protocol tests pass for stdio and local HTTP. That establishes the server's
interface, not successful integration with all of these product interfaces.
Cloud connectors call from a provider's infrastructure. Allowing a browser
origin on localhost is not a route from that cloud to the laptop.

## ChatGPT demonstration — complete before class

Official OpenAI documentation supports private local MCP through Secure MCP
Tunnel. Tunnels and ChatGPT custom-MCP permissions are separate prerequisites;
availability on the actual account/workspace must be verified. Do not spend
class time provisioning them.

1. Give the local agent the setup prompt in `AGENT_SETUP.md`. It runs
   `setup-workshop.py` to prepare dependencies, check the server and publish page data.
2. Have the agent start the existing `start-local.py` launcher
   (`uv run python start-local.py` is the command reference). Keep the loopback endpoint at
   `http://127.0.0.1:8765/mcp`; no inbound public listener is required for the tunnel.
3. Have the appropriate Platform organization/workspace operator create or reuse
   a tunnel and associate it with the intended ChatGPT workspace. Tunnel creation
   needs Read + Manage; runtime use needs Read + Use.
4. Follow the current [Secure MCP Tunnel guide](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
   to install/configure `tunnel-client` for the local HTTP URL and named profile.
   Run its `doctor --explain` check and keep `tunnel-client run` healthy. Use the
   current CLI help for exact profile syntax; no tunnel or key is provisioned by
   this repository. Keep literal keys outside slides, recordings and shared files.
5. In ChatGPT's custom MCP connection flow, select the associated Tunnel and
   configure the required authentication. Install/enable the resulting connection
   in the rehearsal chat. UI names are subject to change; follow the live page.
6. Confirm discovery of `data_status`, `search_documents`, `get_document`. These
   custom tool names are supported by the documented custom-MCP interface; they
   do not need to be renamed `search`/`fetch` for this demonstration.
7. Run the exact climate prompt in [the exercises](EXERCISES.md), expand the tool
   payloads, and verify source/page/answer agreement. Record the model name the
   UI shows, date, connection route and any errors.
8. Re-ingest windows and confirm a fresh tool call sees the changed records.
   Restore page mode, then capture a short successful screen recording as backup.

Do not call this route verified until the actual ChatGPT tool call and inspected
answer succeed. A successful local protocol test is a separate checkpoint.
The native OpenAI tunnel is for supported OpenAI products; it is not a universal
cross-provider tunnel. The current loopback server has no user authentication:
do not expose it publicly as-is through a generic public tunnel.

## Attendees using other clients

Prepare one tested local-agent setup and one local-client route as fallbacks. Use absolute paths from
`mcp.example.json`; a stdio client starts/stops the process itself. For an HTTP
client that makes requests locally, use the loopback endpoint and allow only its
specific browser origin if needed. Keep all three tool names unchanged.

Claude's remote custom connectors operate from Anthropic's cloud; its Desktop
local configuration is a distinct mechanism. Gemini CLI documents both local
process and HTTP MCP connections. These provide concrete alternative routes,
not a claim about the Gemini website or all Claude product surfaces.

Before distributing the guide, personally test one alternative with the same
source question and inspect the tool call. During class, anyone without a
working personal connection can join a prepared pair and still run ingestion
and compare the evidence. Avoid provisioning several cloud integrations live.

## Sources

- [OpenAI: add a custom MCP server](https://developers.openai.com/api/docs/guides/custom-mcp-server)
- [OpenAI: Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
- [Claude: remote connector network requirements and local Desktop distinction](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Gemini CLI: MCP configuration and transports](https://geminicli.com/docs/tools/mcp-server/)
