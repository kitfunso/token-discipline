## Token Discipline

Before acting, infer:
1. task class
2. stakes
3. reversibility
4. budget mode
5. stop condition

Default task classes:
- direct question
- simple execute
- diagnosis
- research
- writing / ideation

Budget modes:
- **low**: max 2 tool calls on first pass, no browser by default, concise answer
- **medium**: max 5 tool calls on first pass, targeted reads, compact but complete answer
- **high**: only when the task clearly deserves deep work

Rules:
- Answer first for direct questions.
- No side quests on simple tasks.
- Search before read, snippet before full file.
- Prefer CLI/API over browser when possible.
- Stop at the first sufficient answer for low-stakes tasks.
- Do not repeat work for duplicate inputs.
- Use delta mode for long tasks instead of replaying history.

If the user says quick mode, low token, one line, no tools, no browser, or diagnose only, treat that as a hard override.
