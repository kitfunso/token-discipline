# Before / After

This file shows target behavior shifts for `token-discipline`.
These are examples of the intended delta, not measured benchmark claims.

## Example 1: Direct question

**Prompt:** `Did we push it yet?`

**Typical wasteful run**
- checks multiple surfaces
- explains the checking process
- answers late

**Target disciplined run**
- answers in the first sentence
- uses at most one quick check if needed
- stops in 1-3 lines

**Expected delta**
- lower latency
- fewer tool calls
- shorter answer

## Example 2: Cheap diagnosis

**Prompt:** `Why is GitHub still showing the old version?`

**Typical wasteful run**
- checks repo, release page, browser, README, npm, and API
- keeps expanding the search surface
- writes a long explanation before naming the likely cause

**Target disciplined run**
- asks what surface is actually stale
- checks the most likely source first
- reports the likely cause and the next step
- escalates only if the cheap path is inconclusive

**Expected delta**
- fewer redundant checks
- less context churn
- faster path to a useful answer

## Example 3: Writing

**Prompt:** `Give me 3 concise X drafts.`

**Typical wasteful run**
- produces 10 options
- includes commentary about tone strategy
- overexplains the choices

**Target disciplined run**
- gives 2-5 strong options
- fits the channel
- avoids brainstorming sprawl

**Expected delta**
- shorter output
- less user scanning cost
- better fit to the actual request
