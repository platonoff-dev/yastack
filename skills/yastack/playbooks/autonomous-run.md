# Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero).
2. Pick the wake mechanism using the `auto-goal` skill, load it with `Skill`, with the exit condition as the goal's condition. An event to watch (CI, a merge, a ref advancing) gets a watcher subagent that wakes you on the event, with a long time-based heartbeat as fallback. No event gets a fixed-interval heartbeat sized to when the result is worth re-checking.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via the `sequence-verifiable-units` principle, verifying each unit before the next instead of batching checks at the end.
4. Mid-run discoveries that support the goal are yours. Address broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift yourself via yastack. Put out-of-band fixes in their own PR. Decide reversible work yourself. Do not ask the user about it, in text or with `AskUserQuestion`. Ask only before an irreversible action, for a product or preference call no experiment can settle, or at a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. Checkpoint every iteration via the `show-me-your-work` skill, loaded with `Skill`, a row for what changed and whether the predicate moved. Claude Code compacts the context as it fills, so a long context is not a reason to wrap up. After a compaction, read the checkpoint log and `git log` before the next iteration.
6. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory. Leave a deliberate block alone and report it, such as a denied permission or a file marked off-limits.
   End a turn only to wait for a wake you set in step 2, or at one of these stops. None of these is a stop: a summary that names the next step, an offer to continue, a list of decisions that block nothing, or a report because the run is long or reached a milestone. Put a status note in the same message as the next tool call.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state, and what waits on the user: a held irreversible action, an open product call, a dead end, or a deliberate block.
