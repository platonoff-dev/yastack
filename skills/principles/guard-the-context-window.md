# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
<!-- markdownlint-disable-next-line MD032 -->
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
