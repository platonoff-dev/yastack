# Bug fix

**You own this task. Plan, review, verify.** Delegate investigation and the fix to subagents, stay in the lead. Use subagents. Choose each subagent's reasoning level for the job. Always use standard speed, never fast. Run subagents locally, never in a cloud environment.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself on the matching surface via the matching control skill, `control-cli` for CLIs and TUIs or `control-ui` for browser, Electron, and web UIs, even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with a trace of the affected subsystem and the `why` skill for regression history. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt with the `auto-goal` skill, with the condition that runtime evidence confirms one surviving mechanism and rules out the other candidate hypotheses. Confirm the surviving *mechanism* with runtime evidence before the step-3 `architect` or `interrogate` fan-out.
3. Plan the fix. If it crosses a function boundary, run the `architect` skill first. Delegate implementation to a subagent with `Agent`, with a specific scope. Pass the absolute path of this playbook and tell the subagent to read it first.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history. See the `tdd` skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical `sequence-verifiable-units` principle, the failing test first and the fix on top.
6. Read the [Opening a PR](opening-a-pr.md) playbook with `Read` and run it.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
