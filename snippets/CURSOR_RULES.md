# Token Discipline Rules

Use proportional effort.

## Route the task
Classify each request as one of:
- direct question
- simple execute
- diagnosis
- research
- writing / ideation

## Choose a budget
### Low
- max 2 tool calls on first pass
- no browser by default
- minimal file reads
- concise output

### Medium
- max 5 tool calls on first pass
- targeted reads only
- browser only if cheaper paths fail

### High
- only for difficult, risky, or explicitly deep work

## Stop rules
- answer direct questions first
- stop at first likely root cause for low-stakes issues
- do not re-verify the same claim repeatedly
- do not reread large files if a snippet is enough
- do not repeat work for duplicate prompts
- use compact summaries and delta updates on long tasks
- direct user messages pre-empt background smoke tests, evals, and diagnostics
- run smoke tests, benchmarks, evals, and other noisy probes in isolated sessions only
- if background work is still running when a new user message arrives, answer the user first, then resume, isolate, or cancel the background work

## Output
Keep answers as short as the task allows.
Do not narrate obvious steps.
Do not overexplore unless the user asked for depth.
