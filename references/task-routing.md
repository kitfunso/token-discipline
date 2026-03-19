# Task Routing

`token-discipline` starts by classifying the task.

## 1. Direct question
Use when the user is clearly asking for a fact, status, or quick judgment.

Examples:
- Did we push it yet?
- Is this live?
- What broke?

Default:
- answer first
- no tools unless essential
- 1-3 lines

## 2. Simple execute
Use when the user wants a concrete action with limited ambiguity.

Examples:
- publish this release
- write three drafts
- update the version

Default:
- do it directly
- minimal narration
- one verification pass

## 3. Diagnosis
Use when the user wants cause-finding.

Examples:
- why is this still showing old data?
- why did this fail?

Default:
- shortest dependency chain first
- stop at likely root cause for low-stakes cases

## 4. Research
Use when the user wants comparison, analysis, or design thinking.

Default:
- deeper work allowed
- more structure allowed

## 5. Writing / ideation
Use for copy, naming, and drafting tasks.

Default:
- few strong options
- avoid brainstorming sprawl
