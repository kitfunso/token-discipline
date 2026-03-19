# Launch Drafts

## Short X post
Most AI agent waste is not model stupidity.
It is effort mismatch.

They read too much, verify too much, and turn simple questions into investigations.

I put together `token-discipline`, a small public framework for task-aware token budgeting:
- route the task
- pick a budget
- use the cheapest adequate path
- stop when enough is enough

## Slightly punchier X post
AI agents do not just need better memory.
They need better judgment about how much work a task deserves.

`token-discipline` is a small framework for making agents:
- cheaper
- faster
- less verbose
- less likely to over-investigate simple tasks

## GitHub launch blurb
`token-discipline` is a small public framework for making AI agents use proportional effort.

It gives agents a simple operating policy for:
- task routing
- budget modes
- stop rules
- tool selection order
- concise-first outputs

The goal is simple: stop agents from treating every task like an investigation.

## Product Hunt / README intro variant
Most prompt files say “be concise.”
That is not enough.

Agents waste tokens because they do not know how much effort a task actually deserves.

`token-discipline` gives them a better default: route the task, choose a budget, use the cheapest adequate path first, and stop once the user’s need is satisfied.
