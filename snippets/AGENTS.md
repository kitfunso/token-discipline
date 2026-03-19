## Token Discipline

### Task routing
Classify each request before acting:
- direct question
- simple execute
- diagnosis
- research
- writing / ideation

### Budget modes
- **low**: max 2 tool calls on first pass, no browser by default, no full-file reads unless necessary, reply <=120 words unless asked for detail
- **medium**: max 5 tool calls on first pass, targeted reads only, browser only if cheaper checks fail
- **high**: only for explicit research, deep debugging, architecture, audits, or high-stakes tasks

### Hard defaults
- Answer direct questions in the first sentence.
- Do not use tools for direct questions unless essential.
- Search before read, snippet before whole file.
- API/CLI before browser when possible.
- Stop after the first likely root cause for low-stakes diagnosis.
- Do not verify the same claim multiple ways unless stakes justify it.
- Do not replay full history on follow-ups. Use deltas.
- Do not rerun work for duplicate queued messages.

### Output defaults
- direct question: 1-3 lines
- simple execute: short confirmation + result
- diagnosis: cause first, then fix/next step
- writing: 2-5 strong options

### Escalation
If the cheap path is inconclusive, explicitly say you are escalating and why.
