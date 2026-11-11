-- Earlier OpenCode database layout: session + message + part.
CREATE TABLE session (id text PRIMARY KEY, project_id text NOT NULL, parent_id text, slug text NOT NULL,
  directory text NOT NULL, title text NOT NULL, version text NOT NULL, time_created integer NOT NULL, time_updated integer NOT NULL);
CREATE TABLE message (id text PRIMARY KEY, session_id text NOT NULL, time_created integer NOT NULL, time_updated integer NOT NULL, data text NOT NULL);
CREATE TABLE part (id text PRIMARY KEY, message_id text NOT NULL, session_id text NOT NULL, time_created integer NOT NULL, time_updated integer NOT NULL, data text NOT NULL);
INSERT INTO session VALUES ('ses_v1demo', 'proj_demo', NULL, 'demo', '/tmp/demo', 'Demo', '1.0.0', 1794132000000, 1794132060000);
INSERT INTO message VALUES ('msg_1', 'ses_v1demo', 1794132000000, 1794132000000, '{"role": "user", "time": {"created": 1794132000000}}');
INSERT INTO message VALUES ('msg_2', 'ses_v1demo', 1794132005000, 1794132005000, '{"role": "assistant", "time": {"created": 1794132005000}}');
INSERT INTO part VALUES ('prt_1', 'msg_1', 'ses_v1demo', 1794132000000, 1794132000000, '{"type": "text", "text": "Why is the server not showing any tools?"}');
INSERT INTO part VALUES ('prt_2', 'msg_1', 'ses_v1demo', 1794132000001, 1794132000001, '{"type": "text", "text": "SYNTHETIC FILE CONTENT", "synthetic": true}');
INSERT INTO part VALUES ('prt_3', 'msg_2', 'ses_v1demo', 1794132005000, 1794132005000, '{"type": "step-start"}');
INSERT INTO part VALUES ('prt_4', 'msg_2', 'ses_v1demo', 1794132005001, 1794132005001, '{"type": "tool", "tool": "bash", "callID": "c1", "state": {"status": "error", "input": {"command": "which uv"}, "error": "uv: command not found"}}');
INSERT INTO part VALUES ('prt_5', 'msg_2', 'ses_v1demo', 1794132005002, 1794132005002, '{"type": "text", "text": "uv is not on the PATH; put its full path in the server settings."}');
