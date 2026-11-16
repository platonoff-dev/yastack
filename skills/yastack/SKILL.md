---
name: yastack
description: Entry point to yastack. Matches the task to a playbook and loads the skills its steps need. Use as /yastack <task>.
disable-model-invocation: true
---

# yastack

The user started this task through yastack. Route it, then do it.

Skills in this stack never load on their own. You load one by reading its file, only when a route below or a playbook step names it. Paths are relative to this file: playbooks at `playbooks/<name>.md`, skills at `../<name>/SKILL.md`.

## Route

1. Match the task to one playbook in the table below. If two fit, take the narrower one.
2. In your first message, name the playbook you picked and why, in one line. If none fits, say so.
3. Read the playbook in full. Copy its steps into your todo list verbatim, before any task-specific items. A step you skip stays in the list with `skip: <reason>`.
4. When a step names a skill, read that skill's `SKILL.md` in full at that step, not earlier, and follow it.
5. No playbook fits: do the task without one. End your final reply with one line, `yastack gap: <the kind of task this was>`, so the user can decide whether it deserves a playbook.

The user's own instructions in the task, `AGENTS.md`, or `CLAUDE.md` override a playbook step. Say which step you overrode.

## Delegating

A subagent can't run slash commands and doesn't know this stack. When a step delegates, put the absolute path of the playbook or skill file in the brief and tell the subagent to read it first. The subagent does not route. It does the step it was given.

## Playbooks

| playbook | use for |
| --- | --- |
| `opening-a-pr` | Open, update, or stack a GitHub pull request or GitLab merge request: clean the diff, shape commits, write the title and body, open ready. |

## Skills

| skill | what it does |
| --- | --- |
| `technical-writing` | Layered writing standard for docs, READMEs, PR descriptions, and commit messages. Applies `unslop-prose` last. |
| `unslop-comments` | Spawn a fresh-context subagent to delete excess comments from a diff, then review its deletions. |
| `unslop-code` | Remove AI slop from the code a branch adds: narrating comments, needless defensive code, type-checker escapes, deep nesting, dead code. |
| `unslop-prose` | Cut AI tells from prose: PR descriptions, commit messages, docs. |
