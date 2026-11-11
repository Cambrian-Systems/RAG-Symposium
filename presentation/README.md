# Two-hour workshop rehearsal kit

The attendee path is **one local-agent prompt → data loaded → tools connected →
answer supported**. Begin with [the setup prompt](AGENT_SETUP.md), then follow
[the participant exercises](EXERCISES.md). A one-command fallback uses the same
setup script when an attendee has no prepared local agent.

For presenters:

- [Run of show](RUN_OF_SHOW.md): 120 minutes, roles, checkpoints and recovery.
- [Slide script](SLIDE_SCRIPT.md): narration, handoffs and technical command references in notes.
- [Agent setup guide](AGENT_SETUP.md): exact setup sequence and truthful verification.
- [Client setup](CLIENT_SETUP.md): ChatGPT preflight and compatible alternatives.
- [Weekend checklist](REHEARSAL.md): prework, handoffs and a full timed practice run.
- [Retrieval snapshot](retrieval-snapshot.json): observed tool-level results from `70695d5`, not generated answers.

The live rehearsal deck is delivered beside the chat. Its main slides show the
agent prompts and evidence checkpoints; detailed commands live in the setup guide
and speaker notes. The Markdown script preserves the notes for repo review.

Instructor-only retrieval check, independent of a language model:

```sh
uv run python presentation/check_demo.py
```

Account-specific connection setup, one tested local-agent route and a full timed
rehearsal still need verification before teaching the session.
