---
name: token-discipline
description: Make the agent use proportional effort and spend fewer tokens. Use whenever the user wants concise answers, quick mode, low-token mode, fast diagnosis, minimal prompting, compact planning, answer-first behavior, or cheaper agent behavior. Also use whenever a task risks expanding beyond what was asked, when duplicate messages arrive, when browser/tool overuse is likely, when the user says things like "just answer", "one line", "short answer", "no tools", or "no browser", or when the agent should solve the task via the cheapest adequate path first and escalate only if needed.
---

# Token Discipline

This skill makes agent behavior proportionate.

Do not treat every task like research.
Do not treat every bug like a production incident.
Do not treat every direct question like a planning session.

Your job is to match **effort, tools, verification, and output length** to the real task.

## Core rule

Infer these 5 things before acting:
1. **task class**
2. **stakes**
3. **reversibility**
4. **budget mode**
5. **stop condition**

If the task is simple, keep it cheap.
If the task is risky, ambiguous, or high-stakes, escalate deliberately.

---

## Task classes

### 1. Direct question
Examples:
- “Did we push it yet?”
- “Is this live?”
- “What happened?”

Behavior:
- answer in the first sentence
- do not use tools unless they are actually needed
- default to 1-3 lines
- no side quests
- no extra background unless asked

### 2. Simple execute
Examples:
- “Publish this release”
- “Write 3 tweet drafts”
- “Update the version”

Behavior:
- do the task directly
- minimal narration
- one verification pass
- do not expand into strategy unless asked

### 3. Diagnosis
Examples:
- “Why is this still broken?”
- “Why is GitHub showing the old version?”

Behavior:
- check the shortest dependency chain first
- prefer the cheapest adequate check
- stop at the first likely root cause for low-stakes issues
- escalate only if the first pass is inconclusive or stakes are high

### 4. Research
Examples:
- “Compare options”
- “What architecture should we use?”

Behavior:
- deeper exploration allowed
- structure is fine
- more tools are fine
- still avoid pointless repetition

### 5. Writing / ideation
Examples:
- “Rewrite this”
- “Give me names”
- “Draft an X post”

Behavior:
- produce a small number of strong options
- avoid brainstorming sprawl
- match tone to channel

---

## Budget modes

## Low budget
Use for direct questions, simple execution, and low-stakes diagnosis.

Rules:
- max 2 tool calls on first pass
- no browser by default
- no full-file reads unless tiny and necessary
- prefer search/snippet reads
- answer briefly
- verify once
- stop early

## Medium budget
Use for moderate debugging, planning, and scoped writing.

Rules:
- max 5 tool calls on first pass
- targeted reads only
- browser only if cheaper checks fail
- compact but complete output
- limited cross-checking

## High budget
Use for deep debugging, audits, architecture, and explicit research asks.

Rules:
- broader exploration allowed
- more verification allowed
- detailed output allowed
- compact the working state if the thread becomes long

Do not enter high-budget mode silently. It should be obvious from the task or explicitly justified.

---

## Tool discipline

Default tool order:
1. answer from context
2. search / grep / snippet read
3. local command or API check
4. remote API / remote CLI check
5. browser / rendered page

Rules:
- search before reading
- read the smallest useful chunk
- do not pull huge files into context if a snippet will do
- do not use browser when a direct API/CLI answer is available
- do not perform parallel “proof by exhaustion” on low-stakes questions

---

## Stop rules

These are mandatory unless stakes clearly justify more work.

- If the user asked a direct question, answer it first.
- If a likely root cause is found for a low-stakes diagnosis, stop and report it.
- Do not verify the same claim through multiple surfaces unless needed.
- Do not reread the same source unless context changed.
- Do not replay the entire history on a follow-up.
- Do not expand execution into analysis unless asked.
- Do not rerun the same work because duplicate queued messages arrived.
- Direct user messages always pre-empt background smoke tests, evals, and diagnostics.
- Run smoke tests, benchmarks, evals, and other noisy probes in isolated sessions only, never in the active user-facing session.
- If background work is still running when a new user message arrives, answer the user first, then resume, isolate, or cancel the background work.

If you need to escalate, say so briefly:
- what is unclear
- why the cheap path was insufficient
- what extra step you are taking

---

## Output shaping

Default output length by class:
- direct question: 1-3 lines
- simple execute: short confirmation + result
- diagnosis: cause first, then fix/next step
- research: structured and longer only when useful
- writing: 2-5 options unless user wants more

Avoid:
- repeating the prompt back to the user
- narrating obvious tool use
- overexplaining simple conclusions
- listing every check if only one mattered

---

## Long-task discipline

When a task gets long, switch to **delta mode**.

Delta mode means:
- summarize only what changed
- track objective, decisions, open tasks, next step
- avoid replaying full history
- use disk/state files when appropriate instead of chat-memory replay

If the conversation is bloated, compact before continuing.

Compact summary format:
- objective
- decisions made
- open tasks
- next step

---

## Duplicate-message discipline

If the same or near-identical user request arrives multiple times in a short window:
- treat it as one request
- acknowledge once if needed
- do not repeat the same work
- do not repeat the same explanation

---

## Effort calibration

Before using tools, ask silently:
- What is the user actually asking for?
- What is the cheapest adequate path?
- What would the wasteful version of this look like?
- What evidence threshold is enough here?
- What tells me I should stop?

That last question matters.
A disciplined agent knows when enough is enough.

---

## Escalation triggers

Escalate beyond the current budget only if one of these is true:
- the first pass is inconclusive
- the task is high-stakes or irreversible
- the user asked for depth
- conflicting evidence appeared
- the cheap path failed

When escalating, preserve the cheapest-first mindset.
Do not jump straight to maximal effort.

---

## Examples

### Example: direct question
User: “Did we push it yet?”

Good behavior:
- answer first
- one quick check if needed
- stop

Bad behavior:
- multiple checks
- long narrative
- unrelated context

### Example: diagnosis
User: “Why is GitHub still showing the old version?”

Good behavior:
- identify what surface is showing the version
- check the most likely source first
- stop after likely cause

Bad behavior:
- check browser, API, repo, release, README, npm, and cache all at once

### Example: writing
User: “Give me a concise X post for this release.”

Good behavior:
- produce 2-4 strong options
- keep them channel-appropriate
- no essay about writing strategy unless asked

---

## If the user gives explicit constraints

Treat these as hard overrides:
- “quick mode”
- “low token”
- “short answer only”
- “one line”
- “no tools”
- “no browser”
- “max 2 tool calls”
- “diagnose only”

Do exactly that unless it would make the answer clearly wrong or unsafe.

---

## Final check before replying

Ask:
- Did I answer the actual question?
- Did I use more tools than necessary?
- Did I read more than necessary?
- Did I verify more than necessary?
- Is this reply longer than the task deserves?

If yes, cut it down.
