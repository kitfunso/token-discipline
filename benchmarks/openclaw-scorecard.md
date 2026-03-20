# Token Discipline Scorecard

Target platform: `openclaw`

Fill this after running baseline and disciplined sessions on the same prompt set.

| id | class | budget | prompt | baseline tools | disciplined tools | baseline tokens | disciplined tokens | baseline ms | disciplined ms | baseline words | disciplined words | baseline answer-first | disciplined answer-first | answer_first | tool_discipline | stop_rule_compliance | output_fit | overall_usefulness | pass | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | direct_question | low | `Did we push hippo yet?` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | diagnosis | low | `Why is GitHub still showing the old version? Quick mode. No browser unless really needed.` | 1 | 1 | 57994 | 57701 | 7324 | 2642 | 50 | 92 | no | no |  |  |  |  |  |  |  |
| 3 | diagnosis | low | `Read this file and tell me the one line I need to change.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | writing_ideation | low | `Give me 3 concise X drafts for Hippo 0.6.0. Keep it practical, not technical.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | diagnosis | low | `Diagnose only: is this deployment issue real or just cache?` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | direct_question | low | `We have a long thread already. Summarize only what changed since yesterday.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | direct_question | low | `No tools. One line only. Is this a good release note?` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | research | high | `Compare three approaches for building a token-aware agent framework.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | simple_execute | low | `Same message may have arrived three times while you were busy. Do not rerun the work unless necessary.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | diagnosis | low | `Low token mode: tell me if this is safe to deploy, and only say more if you're unsure.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | direct_question | low | `Just answer this. Is 0.6.0 actually live on npm yet?` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | diagnosis | low | `I only want the likely cause, not a full investigation. Why is this badge still stale?` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | direct_question | low | `No browser. Check whether the release tag exists and tell me the result in two lines max.` | 2 | 2 | 87570 | 89028 | 18927 | 17218 | 23 | 18 | no | no |  |  |  |  |  |  |  |
| 14 | diagnosis | medium | `Look through this repo and tell me which file matters most for changing the skill trigger behavior.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | writing_ideation | low | `Give me 2 naming options for this repo and one sentence on which one you'd choose.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | direct_question | low | `Be brief. What changed between the previous release and this one?` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | direct_question | medium | `We are already near the context limit. Continue the task using a compact state summary first.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | diagnosis | low | `I think this simple bug might just be user cache. Please don't overdo it.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | writing_ideation | low | `Write a practical GitHub repo description and 5 topic tags for token-discipline.` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | diagnosis | low | `Quick mode, max 2 tool calls: tell me whether this repo is ready for a first public push.` | 1 | 2 | 58977 | 91139 | 10823 | 12207 | 116 | 94 | no | no |  |  |  |  |  |  |  |

## Notes

- `baseline` and `disciplined` metrics can be auto-filled from parser output.
- `baseline answer-first` and `disciplined answer-first` are inferred from whether the assistant opened with text before any tool call.
- Fill the scoring fields consistently across both runs.
- `pass` is the overall judgment for whether the disciplined run was cheaper without becoming worse.
- Use `notes` for false positives, under-answering, or accidental over-escalation.
