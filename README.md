# yastack

Yes, yet another stack of AI skills. A personal skill stack for Claude Code.

**Tuned for Claude Code only.** pstack is tuned to Cursor. yastack is tuned to Claude Code the same way: skills name Claude Code tools and features directly, such as `Agent` subagents, `AskUserQuestion`, worktree isolation, headless `claude -p` sessions, and `disable-model-invocation`. Nothing here targets another harness.

Two ideas taken from [pstack](https://github.com/cursor/plugins/tree/main/pstack):

- **One entry point.** Type `/yastack <task>`. It matches the task to a playbook and loads only the skills that playbook's steps name.
- **Explicit routing.** `/yastack` matches the task to a playbook, and each step names the skill it needs. The agent and its subagents load that skill with the `Skill` tool. Only the entry point sets `disable-model-invocation: true`. `principles` is an index of short cross-cutting rules that the model may load for any task.

Everything else grows from real use, one observed failure at a time.

## Install

```bash
scripts/install.sh            # symlink skills/* into ~/.claude/skills
scripts/install.sh --uninstall
```

Run it from the main checkout. Skill edits apply live through the symlinks.

## Development

```bash
pre-commit install   # once per clone; the hook is the only gate (no CI)
```

## Layout

- `skills/yastack/`: the entry point, with its playbooks in `playbooks/`.
- `skills/<name>/`: routed skills.
- `scripts/check.py`: validates the stack's invariants.

`CLAUDE.md` has the design and the rules for changing the stack.

## Adopt from pstack

Use `/adopt-skill <pstack URL or path>` from this project. The project skill copies one item, replaces Cursor tools with Claude Code ones, and rejects unmet required dependencies. It lives in `.claude/skills/adopt-skill/`.
