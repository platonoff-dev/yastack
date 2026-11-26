---
name: auto-goal
description: Keep working until a checkable condition holds. Runs the work in a headless `claude -p "/goal ..."` child session, then waits for it and verifies the result.
---

# Auto goal

Use this when work must continue until a condition holds: a stubborn bug hunt, "run until done", a migration with a finish check.

## Write the condition

- State one measurable end state with the check that proves it, such as "`bun test test/auth` exits 0".
- A duration is not a condition. "Work on this for 4 hours" gives the goal nothing to check.
- Keep it under 500 characters.
- Claude Code's evaluator judges from the conversation alone. It cannot run commands or read files. Name a check whose output will appear in the transcript.
- Never relax the condition to declare victory.

## Run the goal

The model cannot set `/goal` in its own session. Run the goal work in a headless child session instead.

1. Write a brief to a file outside the repository, such as your scratchpad. The child starts with no context. Include the goal, the condition, the relevant files, what is already ruled out, what it must not touch, whether it may commit, and what to report at the end. Tell it to work around ordinary errors and failing tools, and to report a denied action or an off-limits file instead of working around it.
2. Generate a session id with `uuidgen | tr A-Z a-z`.
3. From the repository directory, start the child with Bash `run_in_background: true` and `timeout: 7200000`:

   ```sh
   claude -p "/goal <condition>" \
     --session-id <id> \
     --permission-mode auto \
     --append-system-prompt-file <brief> \
     --output-format json > <result.json>
   ```

4. While it runs, do not edit the files it works on. Do independent work or end your turn. The harness notifies you when the command exits. Do not poll or sleep.
5. To check progress, read the child's transcript at `~/.claude/projects/*/<id>.jsonl`. Each goal verdict is a `goal_status` entry with `met` and `reason`.
6. When it exits, read `<result.json>`: `subtype`, `is_error`, `result`, and `permission_denials`. Then run the check yourself and review the child's diff. Do not trust its summary.
7. If the condition does not hold, because the 2-hour timeout hit, an error stopped it, or auto mode denied an action, fix what blocked it and resume the same session in the background. If two resumes in a row end on the same blocker, stop and report it:

   ```sh
   claude -p --resume <id> "/goal <condition>" \
     --permission-mode auto \
     --output-format json > <result.json>
   ```

   The new `/goal` replaces the old one, so the goal is always armed on resume.
8. To stop early, stop the background Bash task.

## Reply

The condition, the child session id, how many runs it took, the final check output, and whether the condition holds.
