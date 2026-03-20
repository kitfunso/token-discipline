# token-discipline

**Token optimization for AI agents through task routing, budget modes, stop rules, and OpenClaw-first integration scaffolding.**

Most agents waste tokens in predictable ways:
- they read too much
- they verify too many times
- they narrate too much
- they treat direct questions like investigations

`token-discipline` gives the agent a cheaper default path:
1. classify the task
2. set the budget
3. use the cheapest adequate tool first
4. stop once the task is satisfied
5. escalate only when the cheap path fails

The goal is not "always do less."
The goal is proportional effort.

## What this repo gives you

- a reusable `SKILL.md`
- copy-paste snippets for `AGENTS.md`, `CLAUDE.md`, Cursor, and system prompts
- an OpenClaw-first install path
- structured eval prompts for benchmark runs
- an install checker for OpenClaw setups
- an OpenClaw trace parser for session and cron JSONL logs
- a benchmark scorecard generator
- a machine-readable OpenClaw policy file for future enforcement work

## Why this exists

Most prompt layers say:
- be concise
- be efficient
- do not waste tokens

That is too vague to shape behavior.

What usually goes wrong instead:
- the agent opens a browser when `grep` or an API check was enough
- the agent reads the whole file when 10 lines mattered
- the agent proves the same fact through CLI, API, and browser
- the agent answers "Did we push it yet?" with a paragraph
- the agent reruns the same work because duplicate messages arrived
- background smoke tests keep talking while a real user is waiting

That burns tokens, latency, and trust.

## 60-second OpenClaw install

1. Copy the skill into your OpenClaw skills directory.

```bash
mkdir -p ~/.openclaw/skills/token-discipline
cp SKILL.md ~/.openclaw/skills/token-discipline/SKILL.md
```

2. Paste the repo snippet into your workspace `AGENTS.md`.

Use:
- `snippets/AGENTS.md`

3. Validate that the install actually contains the core policy markers.

```bash
python scripts/check_openclaw_install.py \
  --skill ~/.openclaw/skills/token-discipline/SKILL.md \
  --agents AGENTS.md
```

4. Run the smoke prompts in `SMOKE_TESTS.md`.

### Expected behavior change

After install, OpenClaw should:
- answer direct questions in the first sentence
- stay short by default in low-budget mode
- prefer search and snippet reads before full-file reads
- prefer API and CLI checks before browser work
- stop after the first likely low-stakes diagnosis
- isolate noisy background evals from active user replies

## Before / after

These are target behavior shifts, not benchmark claims.

| Prompt | Wasteful path | Disciplined path | Target effect |
| --- | --- | --- | --- |
| `Did we push it yet?` | Multiple checks, long narration, answer arrives late | One quick check if needed, answer first, stop | Lower latency, lower token use |
| `Why is GitHub still showing the old version?` | Browser plus API plus repo plus README plus npm | Check the most likely source first, stop at likely cause | Fewer tool calls, less context churn |
| `Give me 3 concise X drafts.` | Brainstorm dump plus writing lecture | 2-5 strong options, no sprawl | Shorter output, better fit to request |

See:
- `examples/before-after.md`
- `SMOKE_TESTS.md`
- `evals/evals.json`

## Core model

Every request should map to:
1. a task class
2. a budget mode
3. a tool ceiling
4. a stop condition
5. an output style

### Task classes

- `direct_question`: answer first, no side quests
- `simple_execute`: do the task, verify once, do not overanalyze
- `diagnosis`: shortest dependency chain first, stop at likely cause
- `research`: allow more depth and more evidence
- `writing_ideation`: produce a small number of strong options

### Budget modes

- `low`: max 2 tool calls on first pass, no browser by default, brief answer
- `medium`: max 5 tool calls on first pass, targeted reads only
- `high`: broader exploration for explicit research, audits, or high-stakes work

### Stop rules

- answer direct questions before investigating
- search before reading
- read snippets before whole files
- do not verify the same claim multiple ways unless stakes justify it
- stop after one sufficient low-stakes diagnosis
- switch to delta mode on long threads
- do not rerun work for duplicate queued messages
- direct user messages pre-empt background smoke tests and evals

Reference docs:
- `references/task-routing.md`
- `references/budget-modes.md`
- `references/stop-rules.md`
- `references/tool-selection-order.md`

## When not to optimize aggressively

Do not force strict low-budget behavior when:
- the task is high-stakes or hard to reverse
- the user explicitly asked for deep research
- conflicting evidence appeared on the first pass
- the work is legal, medical, financial, or production-critical
- the user is explicitly paying for thoroughness rather than speed

The point is better judgment, not a permanent austerity mode.

## Proof and benchmarking

This repo now ships a simple benchmark kit so the policy can be measured instead of only described.

### What to measure

For each prompt, compare baseline vs disciplined runs on:
- tool calls
- answer length
- latency
- answer-first behavior
- stop-rule compliance
- overall usefulness

### Files

- `evals/evals.json`: structured prompts with task class, budget, constraints, and pass criteria
- `benchmarks/README.md`: how to run a proof-oriented benchmark
- `benchmarks/openclaw-scorecard.md`: ready-to-fill scorecard template
- `scripts/parse_openclaw_trace.py`: parses OpenClaw session and cron traces into benchmark metrics
- `scripts/render_benchmark_template.py`: generates a scorecard from the eval set

Typical benchmark flow:

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

## OpenClaw integration path

This repo is OpenClaw-first.

Today it ships:
- a reusable skill
- an OpenClaw install checker
- a machine-readable policy file
- a hook map for future enforcement work

See:
- `integrations/openclaw/README.md`
- `integrations/openclaw/policy.json`

The current repo does **not** ship runtime middleware yet.
It does ship the pieces needed to start wiring real enforcement into OpenClaw:
- request classification
- budget selection
- tool gating
- background-job isolation
- explicit escalation markers

## Repo layout

```text
.
|-- README.md
|-- SKILL.md
|-- SMOKE_TESTS.md
|-- ROADMAP.md
|-- NEXT_STEPS.md
|-- snippets/
|-- references/
|-- examples/
|-- evals/
|-- benchmarks/
|-- integrations/openclaw/
`-- scripts/
```

## Positioning

`token-discipline` is best thought of as:
- a practical drop-in for solo agent users
- a proof-friendly benchmark target
- an OpenClaw-first path toward real enforcement

It is not:
- exact token metering for every provider
- a hard-fail policy engine today
- a replacement for deep work when depth is actually warranted

## Roadmap

Short version:
- `v1.1`: OpenClaw-first quickstart, benchmark kit, install checker, policy file
- `v2`: runtime enforcement inside OpenClaw
- `v3`: telemetry and multi-platform expansion if the complexity is worth it

See `ROADMAP.md` for the current plan.

## License

MIT
