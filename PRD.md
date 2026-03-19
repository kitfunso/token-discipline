# Token Discipline PRD

## 1. Overview

**Product name:** token-discipline

**One-line description:**
A practical framework and drop-in skill for making AI agents spend fewer tokens by matching effort, tools, and verbosity to the actual task.

**Short pitch:**
Most agents waste tokens because they treat every request like a research project. `token-discipline` gives agents a simple operating system for task routing, budget selection, stop rules, and compact response behavior. It is designed to reduce unnecessary tool calls, repeated verification, oversized reads, bloated prompts, and rambling outputs.

**Product form:**
`token-discipline` will be a small public GitHub repo that includes:
- a framework-agnostic method
- an OpenClaw/Claude-style skill
- reusable prompt/policy snippets for common agent frameworks
- examples and eval prompts

This is not just a single skill. The skill is one delivery surface for a more general method.

---

## 2. Problem

AI agents are getting more capable, but they are still bad at proportional effort.

Common failure modes:
- using browser automation when a single local check would do
- reading full files when only 10 lines matter
- re-verifying the same thing multiple times
- treating direct questions as investigation tasks
- expanding simple execution into planning, research, diagnosis, and narration
- repeating work when duplicate queued messages arrive
- carrying too much conversation history forward instead of working from deltas
- producing answers that are much longer than the user asked for

This causes three costs:
1. **Token cost:** context and outputs grow much faster than value.
2. **Time cost:** simple tasks become slow.
3. **Trust cost:** users feel they have to micromanage the agent’s effort level.

The deeper problem is not “agents use too many tokens.”
The deeper problem is: **agents often fail to infer stakes, reversibility, and needed depth from the user’s message.**

---

## 3. Vision

Build a lightweight, portable discipline layer that helps agents:
- decide how much effort a task deserves
- choose the cheapest adequate path first
- stop once the user’s real need is satisfied
- stay concise by default
- escalate only when ambiguity, risk, or complexity actually requires it

The long-term vision is to make token efficiency feel like basic agent hygiene, not a user-managed setting.

---

## 4. Product Goals

### Primary goals
- Reduce unnecessary token spend on everyday agent tasks.
- Make agent behavior feel more proportionate to user intent.
- Give users reusable, public, framework-agnostic rules they can drop into their own setups.
- Encode token discipline as a shareable system, not just a personal preference file.

### Secondary goals
- Improve task completion speed on simple requests.
- Reduce tool overuse.
- Improve user satisfaction by matching response length and effort to the ask.
- Create a credible public artifact others can fork, adapt, and benchmark.

### Non-goals
- Building a full telemetry product in v1.
- Measuring exact token counts across every provider in v1.
- Enforcing behavior through code hooks in v1.
- Replacing model judgment with rigid rules for every situation.
- Optimizing for maximum minimalism at the expense of correctness.

---

## 5. Target Users

### Primary users
1. **Power users of AI coding agents**
   - Use Claude Code, OpenClaw, Codex, Cursor, Windsurf, or similar tools
   - Care about context window, speed, and cost
   - Want more predictable agent behavior

2. **Builders managing multi-agent workflows**
   - Spawn sub-agents or persistent coding sessions
   - Need better work partitioning and cheaper orchestration
   - Want agents to use fewer redundant tool calls and less repeated context

3. **Prompt/policy tinkerers**
   - Maintain `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, system prompts, or skills
   - Want a reusable pattern they can publish or standardize across repos

### Secondary users
- teams adopting AI assistants internally
- founders using agents heavily for product work
- researchers benchmarking agent efficiency

---

## 6. Core Insight

The right abstraction is not “be concise.”
It is **task-aware budget routing**.

A good agent should infer:
- what type of task this is
- how expensive it should be allowed to become
- what evidence threshold is enough
- what the cheapest reasonable path is
- when to stop

So the product should revolve around:
1. **Task classification**
2. **Budget modes**
3. **Stop rules**
4. **Tool selection hierarchy**
5. **Context compaction / delta mode**
6. **Output-length defaults**

---

## 7. Product Principles

1. **Cheap-first, not cheap-only**
   Start with the least expensive adequate path. Escalate only if needed.

2. **Answer-first**
   Direct questions should get direct answers before investigation or narration.

3. **Proportional effort**
   Match depth to stakes, reversibility, and ambiguity.

4. **Snippet before whole file**
   Search first. Read the smallest useful unit.

5. **One verification pass by default**
   Do not prove the same thing five ways unless the stakes justify it.

6. **Delta over replay**
   In long tasks, pass only what changed.

7. **Deduplicate repeated inputs**
   Duplicate queued messages should not trigger duplicate work.

8. **Escalation is explicit**
   Going from low to medium or high effort should be a conscious choice.

9. **Readable and portable**
   Rules should work across frameworks and be simple enough for humans to edit.

---

## 8. User Problems to Solve

### Problem A: The agent over-investigates simple issues
**Example:** user asks why GitHub still shows an old version; agent checks browser, API, releases, commit history, README, npm, and more.

**Need:** a discipline layer that says: check the shortest dependency chain first, stop after likely cause, only verify further if asked.

### Problem B: The agent ignores task shape
**Example:** direct question gets treated like a research task.

**Need:** classify tasks upfront and set default behavior.

### Problem C: The agent carries too much context forward
**Example:** each follow-up restates history and repeats tool output.

**Need:** compact mode and delta-mode rules.

### Problem D: The agent reads too much
**Example:** full README or full browser snapshot when only one line matters.

**Need:** snippet-first reading and hard tool ceilings for low-budget tasks.

### Problem E: The user has to manually say “be concise” every time
**Need:** a public, reusable operating policy that makes concise-first behavior the default.

---

## 9. Solution Summary

`token-discipline` will provide a compact method for agents to route work into one of several task modes and assign default budgets and rules to each.

### Core model
Each request is mapped to:
- a **task class**
- a **budget mode**
- a **tool ceiling**
- a **verification threshold**
- an **output style**

### Proposed task classes
1. **Direct question**
2. **Simple execute**
3. **Diagnosis**
4. **Research**
5. **Writing / ideation**

### Proposed budget modes
- **Low**
- **Medium**
- **High**

Each combination defines what is allowed by default.

---

## 10. V1 Scope

### In scope
1. **Public GitHub repo** for `token-discipline`
2. **README** that explains the method plainly
3. **Core skill** (`SKILL.md`) for OpenClaw/Claude-style use
4. **Reusable policy snippets** for:
   - AGENTS.md
   - CLAUDE.md
   - Cursor rules / generic rules files
5. **Task routing framework**
6. **Budget mode definitions**
7. **Stop rules**
8. **Examples of bad vs good behavior**
9. **Starter eval prompts** to test whether the skill behaves proportionately
10. **A concise PRD / architecture note** for future evolution

### Out of scope for v1
- automatic token counting hooks
- dashboard/telemetry UI
- provider-specific SDK integrations
- command-line linting of prompts
- automatic prompt rewriting middleware
- benchmark suite with statistically robust token scoring

---

## 11. Key Deliverables

### Deliverable 1: README
A public-facing document that explains:
- the problem
- the method
- how to use it
- why agents over-spend tokens
- practical defaults
- how to install/adopt it

### Deliverable 2: SKILL.md
A skill that activates when users ask for:
- concise behavior
- low-token mode
- fast diagnosis
- minimal prompting
- compact planning
- effort proportionality

### Deliverable 3: Snippets
Ready-to-paste blocks for:
- `AGENTS.md`
- `CLAUDE.md`
- `.cursorrules` or equivalent

### Deliverable 4: Examples
Concrete examples showing:
- direct question handling
- diagnosis handling
- research escalation
- duplicate input dedupe
- snippet-first reading
- stopping after likely root cause

### Deliverable 5: Evals
A small set of realistic prompts to test whether the discipline actually changes behavior.

---

## 12. Proposed Repo Structure

```text
token-discipline/
├── README.md
├── PRD.md
├── SKILL.md
├── LICENSE
├── examples/
│   ├── direct-question.md
│   ├── diagnosis.md
│   ├── research-escalation.md
│   ├── duplicate-dedupe.md
│   └── compact-delta-mode.md
├── snippets/
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   └── CURSOR_RULES.md
├── references/
│   ├── task-routing.md
│   ├── budget-modes.md
│   ├── stop-rules.md
│   └── tool-selection-order.md
└── evals/
    └── evals.json
```

---

## 13. Functional Requirements

### FR1: Task classification
The system must define a small set of task classes that are easy to understand and broad enough to cover most agent work.

At minimum:
- direct question
- simple execute
- diagnosis
- research
- writing/ideation

### FR2: Budget mode guidance
The system must define low, medium, and high budget modes with clear differences in:
- allowed tool calls
- acceptable read size
- expected answer length
- verification depth
- escalation conditions

### FR3: Tool selection hierarchy
The system must recommend a cheapest-first tool order.

Example hierarchy:
1. answer from context
2. local search/snippet read
3. local command/API check
4. remote/API check
5. browser/rendered page

### FR4: Stop rules
The system must define explicit stop conditions such as:
- stop after first likely root cause for low-stakes diagnosis
- stop after one sufficient verification pass
- stop after satisfying the direct question
- stop re-running on duplicate queued inputs

### FR5: Output shaping
The system must define concise-first output defaults by task class.

### FR6: Long-context handling
The system must define when to switch into:
- compact summaries
- delta prompts
- disk-based task state instead of chat-history replay

### FR7: Portability
The rules must be understandable and usable outside OpenClaw.

### FR8: Shareability
The repo must be publishable as a clean public artifact with no private workspace assumptions.

---

## 14. Non-Functional Requirements

- **Simple:** understandable by humans in under 10 minutes
- **Portable:** usable across agent frameworks
- **Lightweight:** text-first, no required code for v1
- **Opinionated:** strong defaults, not vague advice
- **Practical:** examples should reflect real agent behavior, not toy prompts
- **Cheap to adopt:** copy-paste setup should be possible

---

## 15. User Stories

### For a power user
- As a heavy AI-agent user, I want the agent to answer direct questions briefly without needing to say “be concise” every time.

### For a debugging workflow
- As a user diagnosing a minor issue, I want the agent to check the most likely cause first and stop once it finds a sufficient explanation.

### For a coding workflow
- As a user working in a large repo, I want the agent to read the smallest useful snippet instead of dragging whole files into context.

### For a multi-agent workflow
- As a user spawning sub-agents, I want each agent to get a compact task brief rather than full conversation replay.

### For a framework maintainer
- As a builder, I want a public repo I can share or fork instead of re-explaining token discipline from scratch.

---

## 16. Task Routing Design

### Task Class 1: Direct Question
**Examples:**
- “Did we push hippo yet?”
- “Is this live?”
- “What’s the issue?”

**Defaults:**
- no tools unless essential
- answer in first sentence
- 1-3 lines
- no side quests

### Task Class 2: Simple Execute
**Examples:**
- “Update this version”
- “Publish the release”
- “Write 3 X drafts”

**Defaults:**
- do the thing
- minimal narration
- one verification pass
- no extra analysis unless requested

### Task Class 3: Diagnosis
**Examples:**
- “Why is this still showing old version?”
- “Why is this broken?”

**Defaults:**
- shortest dependency chain first
- max initial tool ceiling
- stop at likely root cause
- only escalate if the first pass is inconclusive

### Task Class 4: Research
**Examples:**
- “Compare approaches”
- “What’s the best architecture here?”

**Defaults:**
- deeper exploration allowed
- multiple sources okay
- structured output okay
- user should expect more tokens/time

### Task Class 5: Writing / Ideation
**Examples:**
- “Write launch copy”
- “Give me naming ideas”

**Defaults:**
- provide a small number of strong options
- avoid giant brainstorming dumps
- tune style to requested channel

---

## 17. Budget Mode Design

## Low Budget
Use for direct questions, simple execute, and low-stakes diagnosis.

**Rules:**
- max 2 tool calls on first pass
- no browser by default
- no full-file reads unless file is tiny and necessary
- reply under ~120 words unless the user asked for detail
- verify once
- stop early

## Medium Budget
Use for moderate diagnosis, scoped writing, or implementation planning.

**Rules:**
- max 5 tool calls on first pass
- targeted file reads only
- browser only if cheaper options fail
- compact but complete output
- limited cross-checking

## High Budget
Use only for architecture, deep research, tricky debugging, audits, or explicit user request.

**Rules:**
- broader tool usage allowed
- multiple passes allowed
- more detailed outputs allowed
- compaction required if the task becomes long-running

---

## 18. Stop Rules

The product must recommend clear defaults like:
- If the user asks a direct question, answer it before doing anything else.
- If a simple diagnosis finds a likely root cause, stop and report it.
- Do not verify the same claim through CLI, API, and browser unless stakes justify it.
- Do not reread the same file unless context changed.
- Do not rerun work because the same queued message arrived three times.
- Do not expand simple execution into strategy unless asked.
- If the task grows beyond its initial class, explicitly announce escalation.

---

## 19. Example Policies for V1

### Policy: Search before read
Use search or targeted grep first. Read only matching snippets before reading a full file.

### Policy: API before browser
If a remote fact can be confirmed by an API or CLI, do that before using a browser.

### Policy: Delta mode
For iterative tasks, send only what changed, not a full replay of prior context.

### Policy: Compact after threshold
If a conversation grows long, summarize objective, decisions, open tasks, next step, then continue from that summary.

### Policy: Duplicate suppression
If the same request arrives multiple times in short succession, acknowledge once and do not duplicate work.

---

## 20. Success Metrics

### Qualitative success
- Users feel the agent is proportionate and less exhausting.
- Fewer complaints about rambling replies.
- Fewer cases where a simple task turns into an investigation spiral.
- Repo feels broadly useful and shareable.

### Quantitative success for v1
Because v1 is mostly a public method, success metrics will be lightweight:
- repo published with clear README and examples
- skill usable in OpenClaw/Claude-style systems
- at least 10 realistic eval prompts created
- user can copy-paste snippets into their setup in under 10 minutes

### Future metrics
Later versions could benchmark:
- average tool calls per task class
- average tokens per task class
- task completion time
- user-rated proportionality
- unnecessary verification rate

---

## 21. Risks

### Risk 1: Over-optimization makes the agent too shallow
If the system pushes “cheap” too hard, the agent may under-investigate real problems.

**Mitigation:** emphasize cheap-first, not cheap-only, and define escalation triggers.

### Risk 2: Rules become too rigid
Rigid rules may fail on edge cases.

**Mitigation:** keep principles strong but allow judgment.

### Risk 3: Too generic to be useful
If the repo reads like vague productivity advice, nobody will use it.

**Mitigation:** use concrete examples, task tables, and copy-paste snippets.

### Risk 4: Hard to prove value publicly
Without telemetry, the repo may sound right but feel unmeasured.

**Mitigation:** include realistic evals and before/after examples.

---

## 22. Competitive Positioning

Most prompt/policy repos tell agents to be “concise,” “helpful,” or “efficient.”
That is too vague.

`token-discipline` should stand out by being:
- practical rather than philosophical
- task-aware rather than generic
- focused on stopping behavior, not just starting behavior
- portable across tools
- written from real agent failure cases, not abstract prompt theory

---

## 23. Launch Positioning

### Positioning statement
`token-discipline` helps AI agents spend effort where it matters and stop wasting tokens where it doesn’t.

### Short public pitch
AI agents don’t just need better memory. They need better judgment about how much work a task deserves.

### Tagline options
- Task-aware token budgeting for AI agents
- Make agents cheaper, faster, and less verbose
- Stop agents from treating every task like an investigation
- Proportional effort for AI agents

---

## 24. V1 Content Outline

### README sections
1. What problem this solves
2. Core idea: task-aware token budgeting
3. The 5 task classes
4. The 3 budget modes
5. Stop rules
6. Tool selection order
7. Copy-paste installation snippets
8. Examples
9. Eval prompts
10. Limitations and future work

### SKILL.md sections
1. when to trigger
2. routing framework
3. budget mode rules
4. stop rules
5. output shaping
6. escalation rules
7. examples

---

## 25. Example Eval Prompts

V1 should include prompts like:
- “Did we push hippo yet?”
- “Why is GitHub still showing the old version?”
- “Read this file and tell me the one line I need to change.”
- “Give me 3 X drafts for this release.”
- “Investigate whether this production issue is real or just cache.”
- “Summarize only what changed since yesterday.”
- “Quick mode: tell me if this is safe to deploy.”
- “No browser, low token mode, diagnose the likely issue.”

These should be used to test whether the skill produces proportionate behavior.

---

## 26. Roadmap Beyond V1

### V1.1
- stronger eval set
- more examples
- multiple framework-specific variants

### V2
- optional lightweight CLI checker
- benchmark harness for tool-count / token-count comparisons
- reusable compact-summary templates

### V3
- provider-specific integrations
- automatic routing helper or middleware
- analytics and feedback loops

---

## 27. Open Questions

1. Should `token-discipline` remain text-only in v1, or include a tiny helper script for evaluation?
2. Should the repo optimize for OpenClaw first, or stay deliberately neutral in the README and treat OpenClaw as one example?
3. Should we position this as a “skill,” “method,” or “agent operating policy” in public messaging?
4. Should we include benchmark claims in v1, or wait until there is a repeatable eval harness?
5. Should a future version integrate directly with Hippo for compact active-task handoffs?

---

## 28. Recommendation

For v1, ship `token-discipline` as:
- a **public method**
- a **drop-in skill**
- a **copy-paste policy repo**

That is the highest-leverage version.
It is useful immediately, portable across ecosystems, and credible enough to share publicly without overbuilding.

---

## 29. Immediate Next Steps

1. Create the repo skeleton.
2. Draft `README.md` from this PRD.
3. Draft `SKILL.md` with strong trigger language.
4. Write policy snippets for AGENTS/CLAUDE/Cursor.
5. Add 8-12 realistic eval prompts.
6. Review the public positioning and naming.
7. Decide whether to build it first in `C:\Users\skf_s\clawd\token-discipline` or a standalone repo root.
