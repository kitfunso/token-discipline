# Budget Modes

## Low
Use for direct questions, simple execution, and low-stakes diagnosis.

Rules:
- max 2 tool calls on first pass
- no browser by default
- no full-file reads unless necessary
- verify once
- brief answer

## Medium
Use for scoped debugging, planning, and moderate writing.

Rules:
- max 5 tool calls on first pass
- targeted reads only
- browser only if cheaper checks fail
- compact but complete answer

## High
Use for audits, architecture, explicit research, and tricky debugging.

Rules:
- broader exploration allowed
- more verification allowed
- compact long task state

High budget should be intentional, not accidental.
