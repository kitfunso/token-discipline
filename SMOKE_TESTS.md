# Smoke Tests

Use these prompts to verify that `token-discipline` is changing behavior, not just sitting in a file.

## What success looks like

A good run should:
- answer direct questions first
- stay short by default
- avoid unnecessary tools
- stop after the first sufficient diagnosis
- respect hard constraints like `no browser`, `no tools`, or `one line`
- keep background smoke-test noise out of the active user-facing session

## Isolation rule

Run smoke tests, evals, and other noisy probes in isolated sessions only.
If a real user message arrives while background work is running, answer the user first and only then resume, isolate, or cancel the background work.

## Fast OpenClaw validation

1. Validate the install:

```bash
python scripts/check_openclaw_install.py \
  --skill ~/.openclaw/skills/token-discipline/SKILL.md \
  --agents AGENTS.md
```

2. Run smoke tests 1, 2, and 3.
3. If those pass, generate a benchmark scorecard:

```bash
python scripts/render_benchmark_template.py \
  --evals evals/evals.json \
  --output benchmarks/openclaw-scorecard.md
```

---

## Test 1: Direct question

**Prompt:**
`Did we push token-discipline yet?`

**Pass if:**
- answer appears in the first sentence
- reply is 1-3 lines
- no obvious side quest

---

## Test 2: Cheap diagnosis

**Prompt:**
`Why is GitHub still showing the old version? Quick mode. No browser unless really needed.`

**Pass if:**
- checks the most likely source first
- does not fan out into browser + API + repo + README all at once
- stops at likely root cause unless still unclear

---

## Test 3: Hard constraint obedience

**Prompt:**
`No tools. One line only. Is this release note good enough?`

**Pass if:**
- one line only
- no tool use
- no follow-on essay

---

## Test 4: Snippet before full read

**Prompt:**
`Read this repo and tell me the one file I should edit to change the trigger behavior.`

**Pass if:**
- searches first
- reads targeted files only
- does not dump large file contents into context

---

## Test 5: Delta mode

**Prompt:**
`We already have a long thread. Summarize only what changed since the last update.`

**Pass if:**
- provides only the delta
- avoids replaying the full story

---

## Test 6: Writing without sprawl

**Prompt:**
`Give me 3 concise X drafts for token-discipline.`

**Pass if:**
- gives 3 strong drafts
- no giant brainstorm list
- no unnecessary strategy lecture

---

## Recommended manual smoke flow by platform

### OpenClaw

- confirm the skill exists at `~/.openclaw/skills/token-discipline/SKILL.md`
- confirm the workspace `AGENTS.md` includes the token-discipline block
- run tests 1, 2, and 3
- then generate a benchmark scorecard from `evals/evals.json`

### Claude Code

- confirm `CLAUDE.md` contains the token-discipline block
- run tests 1, 2, and 5

### Codex

- confirm `AGENTS.md` contains the token-discipline block
- run tests 1, 2, and 4

### Cursor

- confirm `.cursorrules` contains the token-discipline rules
- run tests 3, 4, and 6

---

## Notes

If a client passes file-install checks but fails these behavior checks, the likely problem is one of:
- the rules file is not actually being loaded
- another stronger prompt is overriding it
- the rule text is too weak for that platform
- the task was too trivial to trigger the intended behavior
