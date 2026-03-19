# token-discipline

**Task-aware token budgeting for AI agents.**

Most agents do not fail because they are dumb.
They fail because they use the wrong amount of effort for the job.

They read too much, verify too many times, narrate too much, and turn simple questions into investigations.

`token-discipline` is a small public framework for fixing that.
It gives agents a practical way to decide:
- what kind of task this is
- how much effort it deserves
- which tools to use first
- when to stop
- how short the answer should be

This repo includes:
- a reusable method
- a drop-in `SKILL.md`
- copy-paste snippets for common agent setups
- examples and starter eval prompts

---

## The problem

Most prompt files say things like:
- be concise
- be efficient
- avoid wasting tokens

That sounds nice. It rarely works.

The real issue is that agents usually lack **proportional effort**.

They often:
- use browser automation when a local check would do
- read a whole file when 10 lines matter
- keep verifying the same thing through 3 different surfaces
- answer direct questions with an essay
- carry too much chat history forward
- rerun work because the same message arrived twice

That burns:
- **tokens**
- **time**
- **trust**

---

## Core idea

Do not tell the agent to “be concise.”
Tell it how to **route the task**.

Every request should map to:
1. a **task class**
2. a **budget mode**
3. a **tool ceiling**
4. a **verification threshold**
5. an **output style**

That is what `token-discipline` provides.

---

## The 5 task classes

### 1. Direct question
Examples:
- “Did we push it yet?”
- “Is this live?”
- “What’s the issue?”

Default behavior:
- answer first
- no tools unless essential
- 1-3 lines
- no side quests

### 2. Simple execute
Examples:
- “Publish this release”
- “Update the version”
- “Give me 3 tweet drafts”

Default behavior:
- do the thing
- minimal narration
- one verification pass
- no extra analysis unless asked

### 3. Diagnosis
Examples:
- “Why is GitHub still showing the old version?”
- “Why is this broken?”

Default behavior:
- shortest dependency chain first
- cheap checks first
- stop at likely root cause
- escalate only if the first pass is inconclusive

### 4. Research
Examples:
- “Compare these approaches”
- “What architecture should we use?”

Default behavior:
- more depth allowed
- more sources allowed
- longer answer is acceptable
- user should expect more spend

### 5. Writing / ideation
Examples:
- “Write launch copy”
- “Give me naming ideas”
- “Rewrite this for X”

Default behavior:
- small number of strong options
- avoid giant brainstorming dumps
- shape tone to channel and task

---

## The 3 budget modes

### Low
Use for direct questions, simple tasks, and low-stakes diagnosis.

Rules:
- max 2 tool calls on first pass
- no browser by default
- no full-file reads unless tiny and necessary
- verify once
- answer briefly
- stop early

### Medium
Use for scoped debugging, planning, and moderate writing work.

Rules:
- max 5 tool calls on first pass
- targeted reads only
- browser only if cheaper checks fail
- compact but complete answer
- limited cross-checking

### High
Use for audits, architecture, deep debugging, and explicit research asks.

Rules:
- broader exploration allowed
- multiple sources okay
- more detailed answers okay
- compact the task state when the thread gets long

---

## Stop rules

This is the heart of the method.

A disciplined agent should:
- answer direct questions before investigating
- stop after the first likely root cause for low-stakes diagnosis
- stop after one sufficient verification pass by default
- not prove the same thing through CLI, API, and browser unless stakes justify it
- search before reading, read snippets before whole files
- not rerun work because duplicate queued messages arrived
- switch to delta mode on long tasks instead of replaying the whole story
- explicitly announce escalation when moving from low to medium/high effort

---

## Tool selection order

Default cheapest-first order:
1. answer from current context
2. local search or snippet read
3. local command or API check
4. remote API / remote CLI check
5. browser / rendered page

If step 2 or 3 gives a strong enough answer, stop.

---

## Quick install

### Option 1: Use the skill
Copy `SKILL.md` into your skills system and trigger it whenever the user wants concise, fast, low-token behavior.

### Option 2: Paste the snippets into your rules files
See:
- `snippets/AGENTS.md`
- `snippets/CLAUDE.md`
- `snippets/CURSOR_RULES.md`

### Option 3: Adopt the method manually
Use the task table, budget modes, and stop rules in your own system prompt or agent operating docs.

---

## Practical examples

### Bad
User: “Why is GitHub still showing the old version?”

Agent:
- checks git status
- checks tags
- checks API
- checks release page
- opens browser
- reads README
- checks npm
- compares commit history
- writes 10 paragraphs

### Better
Agent:
- asks: what is most likely showing the version?
- checks the release/tag or npm badge source first
- finds the likely cause
- reports it in 1-3 lines
- only goes deeper if asked

---

### Bad
User: “Did we push it yet?”

Agent:
- reads multiple files
- checks several remotes
- gives a long narrative

### Better
Agent:
- checks the repo state once if needed
- answers in the first sentence
- stops

---

## What this repo is not

This is not a full telemetry system.
It does not count exact tokens across every provider.
It does not enforce behavior through code hooks in v1.

It is a practical, portable operating policy for better agent judgment.

---

## Repo contents

```text
.
├── README.md
├── PRD.md
├── SKILL.md
├── REPO_METADATA.md
├── LAUNCH_DRAFTS.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── snippets/
├── references/
├── examples/
└── evals/
```

Useful starting points:
- `SKILL.md` for skill-based systems
- `snippets/` for copy-paste policy blocks
- `examples/before-after.md` for the simplest explanation of the method
- `LAUNCH_DRAFTS.md` for public sharing

---

## Good fit for

- Claude Code
- OpenClaw
- Codex-style AGENTS setups
- Cursor rules
- Windsurf / Cline / similar agent systems
- any team writing prompt or policy layers for agents

---

## How to use this repo

If you are adopting this for yourself:
1. read `examples/before-after.md`
2. copy one of the snippets into your rules file
3. adapt the budget ceilings to your taste
4. test against prompts in `evals/evals.json`

If you are building a public skill or policy layer:
1. start from `SKILL.md`
2. keep the routing model and stop rules intact
3. customize only the framework-specific wording
4. add your own examples from real failure cases

## Suggested public positioning

**Short pitch:**
AI agents need better judgment about how much work a task deserves.

**Tagline options:**
- Task-aware token budgeting for AI agents
- Stop agents from treating every task like an investigation
- Make agents cheaper, faster, and less verbose
- Proportional effort for AI agents

---

## Future work

Likely next steps:
- small benchmark harness
- before/after evals
- optional helper scripts
- framework-specific variants
- tighter integration with memory systems like Hippo

---

## License

MIT
per scripts
- framework-specific variants
- tighter integration with memory systems like Hippo

---

## License

MIT
