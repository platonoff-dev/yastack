# yastack

Yes, yet another stack of AI skills. A personal skill stack for Claude Code.

**Tuned for Claude Code only.** pstack is tuned to Cursor. yastack is tuned to Claude Code the same way: skills name Claude Code tools and features directly, such as `Agent` subagents, `AskUserQuestion`, worktree isolation, headless `claude -p` sessions, and `disable-model-invocation`. Nothing here targets another harness.

Two ideas taken from [pstack](https://github.com/cursor/plugins/tree/main/pstack):

- **One entry point.** Type `/yastack <task>`. It matches the task to a playbook and loads only the skills that playbook's steps name.
- **Explicit routing.** `/yastack` matches the task to a playbook, and each step names the skill it needs. The agent and its subagents load that skill with the `Skill` tool. Only the entry point sets `disable-model-invocation: true`. `principles` is an index of short cross-cutting rules that the model may load for any task.

Everything else grows from real use, one observed failure at a time.

## Install

yastack is a Claude Code plugin, and the repo is its own marketplace. In Claude Code (2.1.275 or later):

```text
/plugin install yastack --marketplace platonoff-dev/yastack
```

Or from a shell:

```bash
claude plugin marketplace add platonoff-dev/yastack
claude plugin install yastack@yastack
```

Skills are namespaced as `yastack:<skill>`. A bare name still works when no other skill has it, so `/yastack <task>` runs the entry point. The plugin has no `version`, so every commit on `main` is a new version. Run `claude plugin update yastack@yastack` to pull it, or turn on auto-update for the marketplace in `/plugin`.

## Development

```bash
pre-commit install                      # once per clone; the hook is the only gate (no CI)
claude plugin marketplace add "$PWD"    # from the main checkout, instead of the GitHub marketplace
claude plugin install yastack@yastack
claude --plugin-dir .                   # or: load a worktree's copy for one session
```

A local-path marketplace loads the plugin in place, so edits apply on `/reload-plugins` or the next session. A GitHub install is copied into the plugin cache and changes only on update. `--plugin-dir` shadows an installed `yastack` for that session.

## Layout

- `skills/yastack/`: the entry point, with its playbooks in `playbooks/`.
- `skills/<name>/`: routed skills.
- `.claude-plugin/`: the plugin manifest and the single-plugin marketplace.
- `scripts/check.py`: validates the stack's invariants.

`CLAUDE.md` has the design and the rules for changing the stack.

## Adopt from pstack

Use `/adopt-skill <pstack URL or path>` from this project. The project skill copies one item, replaces Cursor tools with Claude Code ones, and rejects unmet required dependencies. It lives in `.claude/skills/adopt-skill/`.
