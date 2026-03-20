# Benchmark Kit

This kit exists to prove that `token-discipline` changes behavior in OpenClaw instead of just sounding good on paper.

## Goal

Compare a baseline run against a disciplined run on the same prompt set and record:
- tool calls
- answer length
- latency
- answer-first behavior
- stop-rule compliance
- overall usefulness

## Inputs

- `evals/evals.json`
- your baseline OpenClaw configuration
- your OpenClaw configuration with `token-discipline` installed
- captured OpenClaw session traces or cron run logs

## Recommended process

0. Keep the workspace context the same between runs.
   The prompt, workspace files, model family, and tool surface should stay constant.
   The only intended variable is whether `token-discipline` is installed and reinforced.
1. Run the eval prompts without `token-discipline`.
2. Save the resulting OpenClaw traces into a baseline folder.
3. Run the same prompts with `token-discipline`.
4. Save those traces into a disciplined folder.
5. Parse both runs:

```bash
python scripts/parse_openclaw_trace.py \
  captures/baseline \
  --evals evals/evals.json \
  --output benchmarks/baseline-report.json

python scripts/parse_openclaw_trace.py \
  captures/disciplined \
  --evals evals/evals.json \
  --output benchmarks/disciplined-report.json
```

6. Merge both reports into the scorecard:

```bash
python scripts/render_benchmark_template.py \
  --evals evals/evals.json \
  --baseline-report benchmarks/baseline-report.json \
  --disciplined-report benchmarks/disciplined-report.json \
  --output benchmarks/openclaw-scorecard.md
```

7. Review the auto-filled scorecard and add the manual judgments:
- answer-first, tool discipline, stop-rule compliance, output fit, and overall usefulness
- overall pass or fail
- any ambiguity or false positives

The repo also includes a checked-in starter file:
- `benchmarks/openclaw-scorecard.md`

## What the parser auto-fills

For session traces, the parser extracts:
- prompt text
- matched `eval_id` when the prompt matches `evals/evals.json`
- tool call count
- unique tool names
- total tokens
- cache read and write tokens
- first-response latency
- completion latency
- final response length

The scorecard generator also auto-fills:
- baseline and disciplined tool counts
- baseline and disciplined token totals
- baseline and disciplined completion latency
- baseline and disciplined final word counts
- inferred baseline and disciplined answer-first flags

For cron run logs, the parser extracts what exists:
- status
- duration
- usage totals
- summary text

Cron logs are useful for hygiene checks.
Session traces are the better source for prompt-level benchmarking.

## Scoring guidance

Use the same standards for both runs.

### `answer_first`
- pass: the direct answer appears immediately
- fail: the answer is buried behind setup or narration

### `tool_discipline`
- pass: the run respects the task budget and cheap-first order
- fail: it fans out early or uses tools the prompt did not justify

### `stop_rule_compliance`
- pass: the run stops after enough evidence for the task
- fail: it keeps checking after the likely answer is already clear

### `output_fit`
- pass: the response length matches the task
- fail: the response is obviously longer or broader than needed

### `overall_usefulness`
- pass: the user would plausibly accept the answer as useful
- fail: the answer is too thin, too noisy, or misses the point

## Rules for honest benchmark data

- do not compare runs if the workspace context or injected files changed materially between baseline and disciplined profiles
- do not invent tool counts or tokens
- do not collapse failed runs into a hand-wavy summary
- include enough notes that another person could rerun the same case
- keep illustrative examples separate from measured results
