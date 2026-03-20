#!/usr/bin/env python3
"""Validate that an OpenClaw token-discipline install contains the required policy markers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_markers(path: Path, label: str, markers: list[str]) -> list[str]:
    issues: list[str] = []
    if not path.exists():
        issues.append(f"{label} missing: {path}")
        return issues

    text = load_text(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        issues.append(f"{label} missing markers:")
        issues.extend([f"  - {marker}" for marker in missing])
    return issues


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_policy = repo_root / "integrations" / "openclaw" / "policy.json"

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--policy",
        type=Path,
        default=default_policy,
        help="Path to the OpenClaw policy file.",
    )
    parser.add_argument(
        "--skill",
        type=Path,
        required=True,
        help="Path to the installed OpenClaw skill file.",
    )
    parser.add_argument(
        "--agents",
        type=Path,
        help="Path to the workspace AGENTS.md file to validate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    policy = json.loads(load_text(args.policy))

    issues: list[str] = []
    issues.extend(
      check_markers(
          args.skill.expanduser(),
          "skill",
          policy.get("required_skill_markers", []),
      )
    )

    if args.agents:
        issues.extend(
          check_markers(
              args.agents.expanduser(),
              "AGENTS.md",
              policy.get("required_agents_markers", []),
          )
        )

    if issues:
        print("OPENCLAW INSTALL CHECK FAILED")
        for issue in issues:
            print(issue)
        return 1

    print("OPENCLAW INSTALL CHECK PASSED")
    print(f"skill: {args.skill.expanduser()}")
    if args.agents:
        print(f"agents: {args.agents.expanduser()}")
    print(f"policy: {args.policy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
