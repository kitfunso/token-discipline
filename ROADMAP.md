# Roadmap

## v1 shipped

- public README
- reusable `SKILL.md`
- AGENTS / CLAUDE / Cursor snippets
- task routing framework
- budget modes
- stop rules
- examples
- starter evals

## v1.1 focus: OpenClaw-first, proof-driven drop-in

- rewrite the repo around token optimization, not generic concision
- make OpenClaw the default quickstart and install path
- add a benchmark kit and scorecard generator
- expand evals into a structured benchmark set
- add stronger before/after and failure-mode examples
- add "when not to optimize aggressively" guidance
- add a machine-readable OpenClaw policy file
- add an install checker for OpenClaw setups
- document concrete OpenClaw hook points for future enforcement

## v2 focus: real runtime enforcement

- wire request classification into the OpenClaw request lifecycle
- wire budget selection and tool ceilings into tool dispatch
- isolate noisy background jobs by default
- expose explicit escalation markers when the cheap path fails
- produce real tool-count and token-count comparison runs from traces
- add policy linting for workspace installs

## v3 focus: telemetry and expansion

- telemetry hooks if the complexity is justified
- dashboards for policy compliance and waste patterns
- provider-specific or platform-specific adapters
- team-level policy packs and governance guidance
