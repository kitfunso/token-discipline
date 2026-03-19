# Stop Rules

A token-disciplined agent stops when the task is satisfied, not when every possible check has been exhausted.

Core stop rules:
- answer direct questions before investigating
- stop after the first likely root cause for low-stakes diagnosis
- stop after one sufficient verification pass by default
- do not verify the same claim through multiple surfaces unless stakes justify it
- do not replay full history on follow-ups
- do not rerun the same work on duplicate prompts
- do not expand execution into analysis unless asked

Escalate only when:
- the first pass is inconclusive
- the task is high-stakes
- the user explicitly wants depth
- the cheap path failed
