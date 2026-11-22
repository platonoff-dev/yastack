# yastack

Yes, yet another stack of AI skills. A personal skill stack for Claude Code and Codex.

Two ideas taken from [pstack](https://github.com/cursor/plugins/tree/main/pstack):

- **One entry point.** Type `/yastack <task>` (Codex: `$yastack <task>`). It matches the task to a playbook and loads only the skills that playbook's steps name.
- **Nothing triggers on its own.** Every skill turns off implicit invocation, so a skill runs only when you call it or `/yastack` routes to it. The one exception is `principles`, an index of short cross-cutting rules that the model may load for any task.

Everything else grows from real use, one observed failure at a time.

## Install

```bash
scripts/install.sh            # symlink skills/* into ~/.claude/skills and ~/.agents/skills
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

`AGENTS.md` has the design and the rules for changing the stack.

## Adopt from pstack

Use `/adopt-skill <pstack URL or path>` in Claude Code or `$adopt-skill <pstack URL or path>` in Codex from this project. The project skill copies one item with minimal adaptations and rejects unmet required dependencies. It lives in `.claude/skills/adopt-skill/`, with a project-local Codex link in `.agents/skills/`.
