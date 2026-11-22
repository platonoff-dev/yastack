---
name: yastack
description: Entry point to yastack. Matches the task to a playbook and loads the skills its steps need. Use as /yastack <task>.
disable-model-invocation: true
---

# yastack

The user started this task through yastack. Route it, then do it.

Skills in this stack never load on their own, except the principles index. You load one by reading its file, only when a non-negotiable, a principle, a playbook step below, or an explicit user request names it. Paths are relative to this file: playbooks at `playbooks/<name>.md`, skills at `../<name>/SKILL.md`, principles at `../principles/<name>.md`.

## Non-negotiables

The principles index grounds every trigger. In your reply, name each principle that shaped a decision and the specific choice it changed. Cite only principles whose file you read this session.

Remaining triggers:

- Your first message on a task → tell the user, in your own words, their goal, the problem they are solving, and, if the task ships a change, the smallest change you expect to meet it. Don't wait for confirmation. If the evidence rules out the change the user asked for, show it and stop. Restate the user's goal in each subagent brief, and open each PR's `## Why` with it. Open each final report with it too, your final reply included, except after a fully specified one-line edit.
- About to ask the user a question on a "which approach", "how should I", or "what should this do" fork → classify it before you ask. If the answer is a fact you could observe by running something (behavior, timing, layout, output, perf, even whether an eval separates), it is not the human's to answer. Sketch it and let the result decide. If the task is a read-only investigation whose deliverable is a cited answer, answer from the evidence rather than building a sketch. Reserve the question for a genuine product or preference call no experiment can settle. Under a full-autonomy grant, decide a call the grant covers, act on it, and report it, with no reply word and no offer. Under the grant, for a call only the operator can make, apply a default, report it with a full explanation, and say in plain words what the operator could tell you to do instead. The operator answers in their own words. Never give a shorthand token to type back. Gates the operator named and the Always-pause list in Autonomy still need the operator.
- Any prose surface, your reply to the user included → the [unslop-prose](../unslop-prose/SKILL.md) skill. Write the reply per **Writing the reply**.
- Docs, RFCs, readmes, PR descriptions, or commit messages → the [technical-writing](../technical-writing/SKILL.md) skill.
- Before commit → the [unslop-code](../unslop-code/SKILL.md) skill.
- Before review → the [unslop-comments](../unslop-comments/SKILL.md) skill.
- Running a benchmark, measuring perf yourself, or reporting a speedup or regression you measured → the [benchmark-checklist](../benchmark-checklist/SKILL.md) skill before you report or act on the number.
- Bugbot or the agentic security review commented → skeptical posture. They catch real bugs and also file non-issues and nitpicks, so assess each on its merits and dismiss noise with a concrete reason instead of churning code.
- Broken skill mid-task → fix it in its own PR. Don't block. Don't silently work around it.

## Principles

Read the [principles](../principles/SKILL.md) index at the start of every task and follow it.

## Autonomy

**Just do it.** Reversible work proceeds without asking.

**Always pause** for irreversible writes and outward-facing actions: force-push to shared branches, deploys, data deletion, customer messages, team chat, ticket updates.

**Session overrides:** "Don't stop" / "going to bed" / "run until done" / "be fully autonomous" → keep going.

**No is an acceptable answer.** Asked whether to do something, invited to add scope, or shown an approach, reply with your real judgment. Decline, push back, or say "this doesn't earn its place" when true. A recommendation is a judgment, not a validation. Agreement is not the default, candor over sycophancy.

## Subagents

A subagent can't run slash commands and doesn't know this stack. When a step delegates, put the absolute path of the playbook or skill file in the brief and tell the subagent to read it first. The subagent does not route. It does the step it was given.

You own every subagent's work. Review the diff and write your own summary, don't pass through what it said. A second opinion is the same prompt against a different model. Agreement is high-signal.

**Fresh subagents by default.** Give new work to a fresh subagent with consolidated scope, meaning the original brief, every later directive, and the prior agent's report and branch. This holds for a fix round, a follow-up, a retry, and the next queue item. Resume, message, or queue a follow-up on an existing subagent only when the new work strictly needs state that lives in that agent and is costly to move: its local checkout, its uncommitted changes, or a process it still runs, such as a dev server or a simulator. A stop or hold order to a running agent is not reuse. A role such as a PR owner outlives its agent. Once that agent returns, a fresh agent takes the role's next round. Interrupt-chained resumes silently drop directives, so fire a fresh subagent with consolidated scope rather than trusting a "done" summary.

## Writing the reply

Write the reply clean as you draft it. A cleanup pass after drafting does not remove these patterns.

- **Short declarative sentences.** One thought per sentence, ended with a period.
- **No long-dash character anywhere.** Write a file-list bullet as a sentence ("`main.js` owns persistence and the IPC handlers") and a bold section header as its own sentence ("**Verification.** End to end via CDP").
- **A colon as a mid-sentence connector is also out** (`unslop-prose` rule 14). A colon before a list is fine.
- **Terse is not an excuse to drop content.** Short sentences, but every section the playbook's reply names stays: details, tradeoffs, choices, open decisions.
- **Frame impact for the consumer and the maintainer.** Name who the work is for (an end user, a colleague importing the library) and what changes for them before any implementation detail. Then what the next engineer who owns this code inherits. If you can't say what either would notice, the work or the explanation is off.
- **Never fabricate a link, citation, or transcript reference.** Link only artifacts you produced or read this session.
- **Every claim carries its evidence or its label in the same sentence.** Measured, inferred, or guess. A prediction or an unseen cause is a guess. Never hand the human a check you could run.

Every playbook ends with a reply written this way, with the PR or MR as a full URL. Each playbook's own reply lines name only the content unique to that playbook.

## Comments

Comments follow the same rule as the reply. Write them clean as you go. Keep a comment only for a non-obvious *why* the code can't show. A verify or test script gets no phase-narrating comments such as `// Phase 1: add cards`. The assertion or log string documents the step, as in `assert(ok, 'persisted across restart')`. This applies to every file you produce, including the delegate's diff.

## Playbooks

Match the task to one playbook below. If two fit, take the narrower one. In your first message, name the playbook you picked and why, in one line. Open its full steps at `playbooks/<name>.md`.

Open a todolist whose first items are the matched playbook's steps, copied in verbatim, before any task-specific todos. A step you choose not to do stays in the list with a one-line `skip: <reason>`. When a step names a skill, read that skill's `SKILL.md` in full at that step, not earlier, and follow it.

No playbook fits → say so in your first message. If the task is a large migration, a change that will land as more than one PR, or a long run the user will review after stepping away, read the [figure-it-out](../figure-it-out/SKILL.md) skill and let it design the playbook. Otherwise do the task without one. Either way, end your final reply with one line, `yastack gap: <the kind of task this was>`, so the user can decide whether it deserves a playbook.

The user's own instructions in the task, or `CLAUDE.md` override a playbook step. Say which step you overrode.

- **Investigation** (`investigation`). A read-only question that needs a cited explanation or a recommendation.
- **Bug fix** (`bug-fix`). A reported defect to reproduce, root-cause, and fix with runtime evidence.
- **Perf issue** (`perf-issue`). A measured slowness to trace and improve against a baseline.
- **Feature** (`feature`). Design, delegate implementation, and verify a new feature.
- **Refactoring** (`refactoring`). A focused-to-medium structural change that preserves behavior against a pinned contract.
- **Opening a PR** (`opening-a-pr`). Open, update, or stack a GitHub pull request or GitLab merge request. Invoked at the end of every other playbook.

## Standalone skills

For an explicit request to run one of these skills, read its linked file.

- [how](../how/SKILL.md). Explain how a subsystem works, including its architecture, runtime flow, and ownership.
- [bro](../bro/SKILL.md). Restate the last message in plain human language, with no jargon.
- [in-your-own-words](../in-your-own-words/SKILL.md). Restate the user's goals and the problem they want to solve.
- [tdd](../tdd/SKILL.md). Make a focused regression fail before a bug fix and pass after it.
- [sharpen](../sharpen/SKILL.md). Make a task deeper, not bigger, then rewrite the prompt.
- [correct](../correct/SKILL.md). Prevent recurring agent mistakes through architecture, types, checks, and tests.
- [arena](../arena/SKILL.md). Spawn parallel candidates, pick a base, and graft the strongest parts into one artifact.
- [architect](../architect/SKILL.md). Sketch types, signatures, and module structure before implementation.
- [swarm](../swarm/SKILL.md). Fan out parallel workers across slices or race arms and return one report.
- [control-cli](../control-cli/SKILL.md). Build or adapt a local harness to drive, inspect, and profile an interactive CLI or TUI.
- [control-ui](../control-ui/SKILL.md). Build or adapt a local browser/CDP harness to drive and inspect a web, IDE, or Electron UI.
- [auto-goal](../auto-goal/SKILL.md). Keep working until a checkable condition holds, with a headless Claude Code `/goal` session.
- [transcript](../transcript/SKILL.md). Find, read, and hand a reviewer the exact transcript of the active run.
- [show-me-your-work](../show-me-your-work/SKILL.md). Keep and audit a reviewable decision trail for long-running or unattended work.
- [figure-it-out](../figure-it-out/SKILL.md). Design and run an auditable workflow when no narrower playbook fits.
