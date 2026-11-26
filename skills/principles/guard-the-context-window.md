# Guard the Context Window

When context fills up with large outputs, long files, repeated reads, or fan-out planning, route the bulk to subagents and keep their summaries in the main thread, not raw payloads.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
<!-- markdownlint-disable-next-line MD032 -->
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
