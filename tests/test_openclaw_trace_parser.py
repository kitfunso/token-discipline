import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OpenClawTraceParserTests(unittest.TestCase):
    def test_parse_session_trace_extracts_metrics(self):
        parser = load_module("scripts/parse_openclaw_trace.py")

        session_lines = [
            {
                "type": "session",
                "version": 3,
                "id": "session-123",
                "timestamp": "2026-03-19T10:00:00.000Z",
                "cwd": "C:\\Users\\skf_s\\clawd\\token-discipline",
            },
            {
                "type": "message",
                "id": "user-1",
                "timestamp": "2026-03-19T10:00:00.000Z",
                "message": {
                    "role": "user",
                    "timestamp": 1000,
                    "content": [{"type": "text", "text": "Did we push hippo yet?"}],
                },
            },
            {
                "type": "message",
                "id": "assistant-1",
                "timestamp": "2026-03-19T10:00:00.500Z",
                "message": {
                    "role": "assistant",
                    "timestamp": 1500,
                    "content": [
                        {
                            "type": "toolCall",
                            "id": "tool-1",
                            "name": "read",
                            "arguments": {"file_path": "C:\\repo\\README.md"},
                        }
                    ],
                    "usage": {
                        "input": 3,
                        "output": 10,
                        "cacheRead": 100,
                        "cacheWrite": 20,
                        "totalTokens": 133,
                    },
                    "stopReason": "toolUse",
                    "provider": "anthropic",
                    "model": "claude-opus-4-6",
                },
            },
            {
                "type": "message",
                "id": "tool-result-1",
                "timestamp": "2026-03-19T10:00:00.700Z",
                "message": {
                    "role": "toolResult",
                    "toolCallId": "tool-1",
                    "toolName": "read",
                    "isError": False,
                    "timestamp": 1700,
                    "content": [{"type": "text", "text": "done"}],
                },
            },
            {
                "type": "message",
                "id": "assistant-2",
                "timestamp": "2026-03-19T10:00:01.200Z",
                "message": {
                    "role": "assistant",
                    "timestamp": 2200,
                    "content": [{"type": "text", "text": "No, not yet."}],
                    "usage": {
                        "input": 2,
                        "output": 4,
                        "cacheRead": 10,
                        "cacheWrite": 5,
                        "totalTokens": 21,
                    },
                    "stopReason": "stop",
                    "provider": "anthropic",
                    "model": "claude-opus-4-6",
                },
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            trace_path = Path(tmp) / "session.jsonl"
            trace_path.write_text(
                "\n".join(json.dumps(line) for line in session_lines) + "\n",
                encoding="utf-8",
            )

            reports = parser.parse_paths([trace_path])

        self.assertEqual(len(reports), 1)
        report = reports[0]
        self.assertEqual(report["kind"], "session")
        self.assertEqual(report["session_id"], "session-123")
        self.assertEqual(report["prompt"], "Did we push hippo yet?")
        self.assertEqual(report["tool_calls"], 1)
        self.assertEqual(report["unique_tools"], ["read"])
        self.assertEqual(report["input_tokens"], 5)
        self.assertEqual(report["output_tokens"], 14)
        self.assertEqual(report["total_tokens"], 154)
        self.assertEqual(report["first_response_ms"], 500)
        self.assertEqual(report["completion_ms"], 1200)
        self.assertEqual(report["final_text"], "No, not yet.")
        self.assertEqual(report["final_word_count"], 3)
        self.assertFalse(report["assistant_opened_with_text"])

    def test_parse_cron_run_extracts_usage_and_duration(self):
        parser = load_module("scripts/parse_openclaw_trace.py")

        cron_lines = [
            {
                "ts": 1772784085166,
                "jobId": "cron-123",
                "action": "finished",
                "status": "ok",
                "summary": "done scanning",
                "sessionId": "session-999",
                "runAtMs": 1772784000015,
                "durationMs": 85146,
                "model": "claude-sonnet-4-6",
                "provider": "anthropic",
                "usage": {
                    "input_tokens": 9,
                    "output_tokens": 3600,
                    "total_tokens": 40836,
                },
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            trace_path = Path(tmp) / "cron.jsonl"
            trace_path.write_text(
                "\n".join(json.dumps(line) for line in cron_lines) + "\n",
                encoding="utf-8",
            )

            reports = parser.parse_paths([trace_path])

        self.assertEqual(len(reports), 1)
        report = reports[0]
        self.assertEqual(report["kind"], "cron_run")
        self.assertEqual(report["session_id"], "session-999")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["tool_calls"], 0)
        self.assertEqual(report["total_tokens"], 40836)
        self.assertEqual(report["completion_ms"], 85146)
        self.assertEqual(report["final_text"], "done scanning")

    def test_parse_session_trace_surfaces_error_status_and_message(self):
        parser = load_module("scripts/parse_openclaw_trace.py")

        session_lines = [
            {
                "type": "session",
                "version": 3,
                "id": "session-error",
                "timestamp": "2026-03-19T22:29:39.165Z",
                "cwd": "C:\\Users\\skf_s\\clawd\\agents\\boring",
            },
            {
                "type": "message",
                "id": "user-1",
                "timestamp": "2026-03-19T22:29:39.597Z",
                "message": {
                    "role": "user",
                    "timestamp": 1000,
                    "content": [{"type": "text", "text": "Run the cron task."}],
                },
            },
            {
                "type": "message",
                "id": "assistant-1",
                "timestamp": "2026-03-19T22:29:42.713Z",
                "message": {
                    "role": "assistant",
                    "timestamp": 2500,
                    "content": [],
                    "usage": {
                        "input": 0,
                        "output": 0,
                        "cacheRead": 0,
                        "cacheWrite": 0,
                        "totalTokens": 0,
                    },
                    "stopReason": "error",
                    "provider": "anthropic",
                    "model": "claude-sonnet-4-6",
                    "errorMessage": "429 rate limit",
                },
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            trace_path = Path(tmp) / "session-error.jsonl"
            trace_path.write_text(
                "\n".join(json.dumps(line) for line in session_lines) + "\n",
                encoding="utf-8",
            )

            reports = parser.parse_paths([trace_path])

        self.assertEqual(len(reports), 1)
        report = reports[0]
        self.assertEqual(report["kind"], "session")
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["error_message"], "429 rate limit")
        self.assertEqual(report["final_text"], "429 rate limit")
        self.assertEqual(report["completion_ms"], 1500)

    def test_render_scorecard_can_merge_parser_reports(self):
        renderer = load_module("scripts/render_benchmark_template.py")

        payload = {
            "benchmark_target": "openclaw",
            "scoring_fields": [
                "answer_first",
                "tool_discipline",
                "stop_rule_compliance",
                "output_fit",
                "overall_usefulness",
            ],
            "evals": [
                {
                    "id": 1,
                    "task_class": "direct_question",
                    "budget_mode": "low",
                    "prompt": "Did we push hippo yet?",
                }
            ],
        }
        baseline_report = {
            "reports": [
                {
                    "eval_id": 1,
                    "tool_calls": 3,
                    "total_tokens": 420,
                    "completion_ms": 1900,
                    "final_word_count": 28,
                    "assistant_opened_with_text": False,
                }
            ]
        }
        disciplined_report = {
            "reports": [
                {
                    "eval_id": 1,
                    "tool_calls": 1,
                    "total_tokens": 120,
                    "completion_ms": 700,
                    "final_word_count": 4,
                    "assistant_opened_with_text": True,
                }
            ]
        }

        markdown = renderer.build_markdown(
            payload,
            baseline_reports=baseline_report,
            disciplined_reports=disciplined_report,
        )

        self.assertIn("baseline answer-first", markdown)
        self.assertIn("disciplined answer-first", markdown)
        self.assertIn("| answer_first | tool_discipline | stop_rule_compliance | output_fit | overall_usefulness | pass | notes |", markdown)
        self.assertIn("| 1 | direct_question | low | `Did we push hippo yet?` | 3 | 1 | 420 | 120 | 1900 | 700 | 28 | 4 | no | yes |  |  |  |  |  |  |  |", markdown)


if __name__ == "__main__":
    unittest.main()
