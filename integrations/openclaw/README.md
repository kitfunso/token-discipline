# OpenClaw Integration

`token-discipline` is OpenClaw-first because OpenClaw already gives you the two most useful policy surfaces:
- installable skills
- workspace rules such as `AGENTS.md`

That makes it the easiest place to prove the value of token discipline before building heavier runtime enforcement.

## What ships now

- skill install path: `~/.openclaw/skills/token-discipline/SKILL.md`
- workspace reinforcement via `snippets/AGENTS.md`
- machine-readable policy file: `integrations/openclaw/policy.json`
- install validation script: `scripts/check_openclaw_install.py`
- trace parser: `scripts/parse_openclaw_trace.py`
- benchmark scorecard generator: `scripts/render_benchmark_template.py`

## Recommended install

```bash
mkdir -p ~/.openclaw/skills/token-discipline
cp SKILL.md ~/.openclaw/skills/token-discipline/SKILL.md
python scripts/check_openclaw_install.py \
  --skill ~/.openclaw/skills/token-discipline/SKILL.md \
  --agents AGENTS.md
```

## Measuring performance

Once you have baseline and disciplined trace captures, generate benchmark reports with:

```bash
python scripts/parse_openclaw_trace.py \
  captures/baseline \
  --evals evals/evals.json \
  --output benchmarks/baseline-report.json

python scripts/parse_openclaw_trace.py \
  captures/disciplined \
  --evals evals/evals.json \
  --output benchmarks/disciplined-report.json

python scripts/render_benchmark_template.py \
  --evals evals/evals.json \
  --baseline-report benchmarks/baseline-report.json \
  --disciplined-report benchmarks/disciplined-report.json \
  --output benchmarks/openclaw-scorecard.md
```

## Hook map

| Hook | Stage | Purpose | Current state |
| --- | --- | --- | --- |
| `request_classifier` | pre-routing | map each request to a task class and budget mode before tools run | documented in `policy.json` |
| `budget_selector` | pre-tool | enforce low / medium / high first-pass ceilings | documented in `policy.json` |
| `tool_gate` | tool dispatch | prefer search, snippets, and API checks before browser work | documented in `policy.json` |
| `background_isolation` | scheduler | keep smoke tests, evals, and other noisy jobs away from live user replies | documented in `policy.json` |
| `escalation_marker` | reply shaping | announce when the agent moves beyond the cheap path | documented in `policy.json` |

## What counts as real enforcement

Docs alone are not enforcement.

For OpenClaw, real enforcement means:
- request classification happens before tool selection
- the current budget is visible to the tool layer
- cheap-first ordering can deny or delay expensive tools
- background jobs can be pre-empted by direct user messages
- escalation is explicit when the agent crosses the first-pass budget

This repo does not ship that runtime code yet.
It does ship the policy file, install checks, and benchmark scaffolding needed to build it without guessing.

## Suggested next implementation steps

1. Load `policy.json` at session start.
2. Stamp each request with `task_class` and `budget_mode`.
3. Add a first-pass tool counter to the session state.
4. Gate browser or rendered-page tools behind the cheap-path failure condition.
5. Mark background smoke tests and evals as lower priority than live user turns.
