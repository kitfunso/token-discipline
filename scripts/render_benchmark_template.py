#!/usr/bin/env python3
"""Render a Markdown benchmark scorecard from evals/evals.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals", type=Path, required=True, help="Path to evals JSON.")
    parser.add_argument(
        "--baseline-report",
        type=Path,
        help="Optional parser output JSON for baseline runs.",
    )
    parser.add_argument(
        "--disciplined-report",
        type=Path,
        help="Optional parser output JSON for disciplined runs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the generated Markdown to this path. Defaults to stdout.",
    )
    return parser.parse_args()


def sanitize(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def index_reports(report_payload: dict | None) -> dict[int, dict]:
    if not report_payload:
        return {}
    indexed: dict[int, dict] = {}
    for report in report_payload.get("reports", []):
        eval_id = report.get("eval_id")
        if isinstance(eval_id, int):
            indexed[eval_id] = report
    return indexed


def metric(report: dict | None, key: str) -> str:
    if not report:
        return ""
    value = report.get(key)
    return "" if value is None else str(value)


def yes_no_metric(report: dict | None, key: str) -> str:
    if not report:
        return ""
    value = report.get(key)
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return ""


def build_markdown(
    payload: dict,
    baseline_reports: dict | None = None,
    disciplined_reports: dict | None = None,
) -> str:
    baseline_index = index_reports(baseline_reports)
    disciplined_index = index_reports(disciplined_reports)
    scoring_fields = [sanitize(field) for field in payload.get("scoring_fields", [])]
    lines: list[str] = []
    lines.append("# Token Discipline Scorecard")
    lines.append("")
    lines.append(f"Target platform: `{payload.get('benchmark_target', 'unknown')}`")
    lines.append("")
    lines.append("Fill this after running baseline and disciplined sessions on the same prompt set.")
    lines.append("")
    header = [
        "id",
        "class",
        "budget",
        "prompt",
        "baseline tools",
        "disciplined tools",
        "baseline tokens",
        "disciplined tokens",
        "baseline ms",
        "disciplined ms",
        "baseline words",
        "disciplined words",
        "baseline answer-first",
        "disciplined answer-first",
    ]
    header.extend(scoring_fields)
    header.append("pass")
    header.append("notes")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    for entry in payload.get("evals", []):
        baseline = baseline_index.get(entry["id"])
        disciplined = disciplined_index.get(entry["id"])
        row = [
            str(entry["id"]),
            sanitize(entry["task_class"]),
            sanitize(entry["budget_mode"]),
            f"`{sanitize(entry['prompt'])}`",
            metric(baseline, "tool_calls"),
            metric(disciplined, "tool_calls"),
            metric(baseline, "total_tokens"),
            metric(disciplined, "total_tokens"),
            metric(baseline, "completion_ms"),
            metric(disciplined, "completion_ms"),
            metric(baseline, "final_word_count"),
            metric(disciplined, "final_word_count"),
            yes_no_metric(baseline, "assistant_opened_with_text"),
            yes_no_metric(disciplined, "assistant_opened_with_text"),
        ]
        row.extend([""] * len(scoring_fields))
        row.append("")
        row.append("")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- `baseline` and `disciplined` metrics can be auto-filled from parser output.")
    lines.append("- `baseline answer-first` and `disciplined answer-first` are inferred from whether the assistant opened with text before any tool call.")
    lines.append("- Fill the scoring fields consistently across both runs.")
    lines.append("- `pass` is the overall judgment for whether the disciplined run was cheaper without becoming worse.")
    lines.append("- Use `notes` for false positives, under-answering, or accidental over-escalation.")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    payload = json.loads(args.evals.read_text(encoding="utf-8"))
    baseline_reports = None
    disciplined_reports = None

    if args.baseline_report:
        baseline_reports = json.loads(args.baseline_report.read_text(encoding="utf-8"))
    if args.disciplined_report:
        disciplined_reports = json.loads(args.disciplined_report.read_text(encoding="utf-8"))

    markdown = build_markdown(
        payload,
        baseline_reports=baseline_reports,
        disciplined_reports=disciplined_reports,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
