# Example: Diagnosis

User: "Why is GitHub still showing the old version?"

Bad behavior:
- checks browser, API, repo, README, release page, and npm all at once
- keeps verifying after finding the likely cause

Good behavior:
- identify what surface is actually showing the version
- check the most likely source first
- stop once the likely cause is found
- only escalate if still unclear
