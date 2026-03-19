# Tool Selection Order

Prefer the cheapest adequate path.

Default order:
1. answer from context
2. search / grep / snippet read
3. local command or API check
4. remote API / remote CLI check
5. browser / rendered page

Guidelines:
- search before read
- snippet before whole file
- CLI/API before browser
- one strong answer is better than five weak confirmations
- only escalate when the current layer is insufficient
