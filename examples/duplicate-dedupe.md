# Example: Duplicate Input Dedupe

User message arrives 3 times while the agent is busy.

Bad behavior:
- reruns the same task 3 times
- restates the same answer 3 times

Good behavior:
- treat it as one request
- acknowledge once if needed
- do not redo completed work unless the user asks for a rerun
