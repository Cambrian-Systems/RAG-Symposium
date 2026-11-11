-- Newest OpenCode layout: session_v2 + session_message (only the columns rag-sessions reads).
CREATE TABLE session_v2 (id text PRIMARY KEY, project_id text NOT NULL, parent_id text, slug text NOT NULL,
  directory text NOT NULL, title text, version text NOT NULL, time_created integer NOT NULL, time_updated integer NOT NULL);
CREATE TABLE session_message (id text PRIMARY KEY, session_id text NOT NULL, type text NOT NULL, seq integer NOT NULL,
  time_created integer NOT NULL, time_updated integer NOT NULL, data text NOT NULL);
INSERT INTO session_v2 VALUES ('ses_v2demo', 'proj_demo', NULL, 'demo', '/tmp/demo', 'Demo', '2.2.7', 1794222000000, 1794222120000);
INSERT INTO session_v2 VALUES ('ses_v2child', 'proj_demo', 'ses_v2demo', 'child', '/tmp/demo', 'Child', '2.2.7', 1794222000000, 1794222120000);
INSERT INTO session_message VALUES ('msg_a', 'ses_v2demo', 'system', 1, 1794222000000, 1794222000000, '{"text": "SYSTEM PROMPT"}');
INSERT INTO session_message VALUES ('msg_b', 'ses_v2demo', 'user', 2, 1794222001000, 1794222001000, '{"time": {"created": 1794222001000}, "text": "Search the documents for AI literacy", "files": []}');
INSERT INTO session_message VALUES ('msg_c', 'ses_v2demo', 'assistant', 3, 1794222002000, 1794222010000, '{"content": [{"type": "reasoning", "text": "PRIVATE REASONING"}, {"type": "tool", "id": "t1", "name": "rag_search_documents", "state": {"status": "completed", "input": {"query": "AI literacy"}, "content": [{"type": "text", "text": "ED-FR-2026-07087-p6 defines AI literacy"}]}}, {"type": "text", "text": "The April 2026 rule defines AI literacy on page 6."}]}');
INSERT INTO session_message VALUES ('msg_d', 'ses_v2demo', 'idle', 4, 1794222011000, 1794222011000, '{"outcome": "done"}');
INSERT INTO session_message VALUES ('msg_e', 'ses_v2child', 'user', 1, 1794222001000, 1794222001000, '{"text": "CHILD SESSION TASK"}');
