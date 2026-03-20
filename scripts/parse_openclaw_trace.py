#!/usr/bin/env python3
"""Parse OpenClaw session or cron JSONL traces into benchmark-friendly metrics."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="JSONL trace files or directories.")
    parser.add_argument("--evals", type=Path, help="Optional evals JSON for prompt matching.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    parser.add_argument("--output", type=Path, help="Write output to this path.")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def iter_trace_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        expanded = path.expanduser()
        if expanded.is_dir():
            files.extend(sorted(expanded.rglob("*.jsonl")))
        elif expanded.is_file():
            files.append(expanded)
    return files


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.lower().split())


def parse_timestamp(value: Any) -> int | None:
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1000)
        except ValueError:
            return None
    return None


def extract_text(content: list[dict[str, Any]] | None) -> str:
    if not content:
        return ""
    parts: list[str] = []
    for item in content:
        if item.get("type") in {"text", "input_text", "output_text"}:
            text = item.get("text")
            if isinstance(text, str) and text.strip():
                parts.append(text.strip())
    return "\n".join(parts)


def assistant_opened_with_text(content: list[dict[str, Any]] | None) -> bool:
    if not content:
        return False
    for item in content:
        item_type = item.get("type")
        if item_type in {"text", "input_text", "output_text"}:
            return bool((item.get("text") or "").strip())
        if item_type == "toolCall":
            return False
    return False


def sum_usage(target: dict[str, int], usage: dict[str, Any] | None) -> None:
    if not usage:
        return
    target["input_tokens"] += int(usage.get("input", usage.get("input_tokens", 0)) or 0)
    target["output_tokens"] += int(usage.get("output", usage.get("output_tokens", 0)) or 0)
    target["total_tokens"] += int(usage.get("totalTokens", usage.get("total_tokens", 0)) or 0)
    target["cache_read_tokens"] += int(usage.get("cacheRead", usage.get("cache_read_tokens", 0)) or 0)
    target["cache_write_tokens"] += int(usage.get("cacheWrite", usage.get("cache_write_tokens", 0)) or 0)


def count_words(text: str) -> int:
    return len(text.split()) if text.strip() else 0


def match_eval_id(prompt: str | None, evals: list[dict[str, Any]] | None) -> int | None:
    if not prompt or not evals:
        return None
    normalized_prompt = normalize_text(prompt)
    candidates: list[int] = []
    for entry in evals:
        candidate = normalize_text(entry.get("prompt"))
        if candidate and (candidate == normalized_prompt or candidate in normalized_prompt or normalized_prompt in candidate):
            candidates.append(entry["id"])
    return candidates[0] if len(candidates) == 1 else None


def parse_session_trace(records: list[dict[str, Any]], path: Path, evals: list[dict[str, Any]] | None) -> dict[str, Any]:
    session = records[0]
    usage_totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
    }
    unique_tools: set[str] = set()
    first_user_ts: int | None = None
    first_user_text: str | None = None
    first_assistant_ts: int | None = None
    last_assistant_ts: int | None = None
    last_assistant_text = ""
    opened_with_text = False
    provider = None
    model = None
    tool_calls = 0
    last_stop_reason: str | None = None
    last_error_message: str | None = None

    for record in records:
        if record.get("type") != "message":
            continue
        message = record.get("message", {})
        role = message.get("role")
        msg_ts = parse_timestamp(message.get("timestamp")) or parse_timestamp(record.get("timestamp"))

        if role == "user" and first_user_ts is None:
            first_user_ts = msg_ts
            first_user_text = extract_text(message.get("content"))
        elif role == "assistant":
            content = message.get("content") or []
            if first_assistant_ts is None:
                first_assistant_ts = msg_ts
                opened_with_text = assistant_opened_with_text(content)
            last_assistant_ts = msg_ts
            provider = message.get("provider") or provider
            model = message.get("model") or model
            last_stop_reason = message.get("stopReason") or last_stop_reason
            last_error_message = message.get("errorMessage") or last_error_message
            sum_usage(usage_totals, message.get("usage"))

            for item in content:
                if item.get("type") == "toolCall":
                    tool_calls += 1
                    name = item.get("name")
                    if isinstance(name, str) and name:
                        unique_tools.add(name)

            text = extract_text(content)
            if text:
                last_assistant_text = text

    if last_stop_reason == "error" or (last_error_message and not last_assistant_text):
        status = "error"
    elif last_stop_reason == "toolUse" and not last_assistant_text:
        status = "incomplete"
    else:
        status = "ok"

    error_message = last_error_message if status == "error" else None
    final_text = last_assistant_text or error_message or ""

    report = {
        "kind": "session",
        "path": str(path),
        "session_id": session.get("id"),
        "prompt": first_user_text,
        "eval_id": match_eval_id(first_user_text, evals),
        "tool_calls": tool_calls,
        "unique_tools": sorted(unique_tools),
        "input_tokens": usage_totals["input_tokens"],
        "output_tokens": usage_totals["output_tokens"],
        "total_tokens": usage_totals["total_tokens"],
        "cache_read_tokens": usage_totals["cache_read_tokens"],
        "cache_write_tokens": usage_totals["cache_write_tokens"],
        "first_response_ms": (first_assistant_ts - first_user_ts) if first_assistant_ts is not None and first_user_ts is not None else None,
        "completion_ms": (last_assistant_ts - first_user_ts) if last_assistant_ts is not None and first_user_ts is not None else None,
        "final_text": final_text,
        "final_word_count": count_words(final_text),
        "final_line_count": len(final_text.splitlines()) if final_text else 0,
        "assistant_opened_with_text": opened_with_text,
        "provider": provider,
        "model": model,
        "status": status,
        "error_message": error_message,
    }
    return report


def parse_cron_trace(records: list[dict[str, Any]], path: Path, evals: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for record in records:
        if record.get("action") != "finished":
            continue
        usage = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "cache_read_tokens": 0,
            "cache_write_tokens": 0,
        }
        sum_usage(usage, record.get("usage"))
        final_text = record.get("summary") or record.get("error") or ""
        report = {
            "kind": "cron_run",
            "path": str(path),
            "session_id": record.get("sessionId"),
            "prompt": None,
            "eval_id": None,
            "job_id": record.get("jobId"),
            "tool_calls": 0,
            "unique_tools": [],
            "input_tokens": usage["input_tokens"],
            "output_tokens": usage["output_tokens"],
            "total_tokens": usage["total_tokens"],
            "cache_read_tokens": usage["cache_read_tokens"],
            "cache_write_tokens": usage["cache_write_tokens"],
            "first_response_ms": None,
            "completion_ms": int(record.get("durationMs", 0) or 0),
            "final_text": final_text,
            "final_word_count": count_words(final_text),
            "final_line_count": len(final_text.splitlines()) if final_text else 0,
            "assistant_opened_with_text": False,
            "provider": record.get("provider"),
            "model": record.get("model"),
            "status": record.get("status"),
        }
        reports.append(report)
    return reports


def parse_paths(paths: list[Path], evals: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for path in iter_trace_files(paths):
        records = read_jsonl(path)
        if not records:
            continue
        first = records[0]
        if first.get("type") == "session":
            reports.append(parse_session_trace(records, path, evals))
        elif "action" in first:
            reports.extend(parse_cron_trace(records, path, evals))
    return reports


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# OpenClaw Trace Report",
        "",
        "| kind | session/job | prompt | tools | total tokens | completion ms | final words | path |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for report in payload.get("reports", []):
        session_or_job = report.get("session_id") or report.get("job_id") or ""
        prompt = normalize_text(report.get("prompt") or report.get("final_text") or "")[:80]
        lines.append(
            "| {kind} | {session_or_job} | {prompt} | {tool_calls} | {total_tokens} | {completion_ms} | {final_word_count} | {path} |".format(
                kind=report.get("kind", ""),
                session_or_job=session_or_job,
                prompt=prompt.replace("|", "\\|"),
                tool_calls=report.get("tool_calls", ""),
                total_tokens=report.get("total_tokens", ""),
                completion_ms=report.get("completion_ms", ""),
                final_word_count=report.get("final_word_count", ""),
                path=str(report.get("path", "")).replace("|", "\\|"),
            )
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    evals_payload = None
    if args.evals:
        evals_payload = json.loads(args.evals.read_text(encoding="utf-8")).get("evals", [])

    reports = parse_paths(args.inputs, evals_payload)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reports": reports,
    }

    if args.format == "markdown":
        output = build_markdown(payload)
    else:
        output = json.dumps(payload, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
