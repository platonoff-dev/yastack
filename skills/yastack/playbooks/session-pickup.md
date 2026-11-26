# Session pickup

**You own the resume point. Read the prior trail, don't redo it.**

1. Locate the prior trail. It is one of these:
   - A local transcript in the active workspace's transcript directory. The `transcript` skill, loaded with `Skill`, resolves this run's transcript, and the prior run's sits in the same directory if it ran in this checkout. A run in another worktree of this repo sits in that worktree's directory, named from its path in `git worktree list`. Do not glob across `~/.claude/projects/*/`, that crosses workspace boundaries and reads private chats from unrelated projects.
   - A Claude Code cloud session URL.
   - A pushed branch.
   - A resume note that a pause left (its path is in the pause reply).

   Read the metadata overview and last messages first, then scan back for the decision points. Parse a long transcript in a subagent and keep the reduced timeline in the main thread (the `guard-the-context-window` principle).
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open checklist items and tasks, the decisions made. The prior trail is authoritative input. Resist the bias to re-derive it.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, and do not redo completed work, such as re-deriving the prior repro. Checking an inherited claim on the real artifact is not redoing it.
4. Verify the inherited claims against the original goal on the real artifact (the `prove-it-works` principle). A passing prior self-report is not the proof.
5. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here. The routed playbook owns the rest.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.
