# AGENTS.md

Guidance for AI agents working in this repository.

## What this repo is

yastack is a personal stack of agent skills for Claude Code and Codex. It borrows three ideas from poteto's pstack and nothing else by default:

1. **One entry point.** The user types `/yastack <task>` and the stack decides which playbook and skills apply. The user never has to remember which skill fits which task.
2. **Explicit routing only.** No skill triggers on its own. Every skill turns off implicit invocation, and the entry point loads skills by reading their files when a route says so. The one exception is the `principles` index, described next.
3. **Principles.** Short rules that cut across playbooks, such as "explain the number before you trust it". They are plain Markdown files under one skill, `principles`, whose `SKILL.md` indexes each one with the condition it applies under. That skill keeps implicit invocation on, so the model can load the index for any task, not only under `/yastack`. The entry point reads the index at the start of every task. The agent reads a principle file when its condition holds or the user names it, and names it in the final reply.

The stack grows by iteration on real use. A skill or playbook earns its place by fixing something that went wrong in an actual session. Skills may be adopted from pstack or elsewhere, but each one is judged first. For pstack, follow `.claude/skills/adopt-skill/SKILL.md`. Keep the source text as close to the original as possible. Reject unmet required dependencies rather than deleting the steps that need them.

The remote is public (`github.com/platonoff-dev/yastack`). Nothing work-specific goes here: no employer systems, people, tickets, hostnames, or secrets. Work skills live in the separate corporate `dotai` repo.

## Layout

```text
skills/
  yastack/                entry point (the router)
    SKILL.md              modeled on pstack's poteto-mode: non-negotiables, principles, autonomy,
                          subagents, reply and comment rules, the playbook list
    playbooks/<name>.md   one procedure per task kind (bug fix, feature, ...)
    agents/openai.yaml    Codex metadata
  <name>/                 a routed skill: a capability that playbooks call
    SKILL.md
    agents/openai.yaml
    ...                   supporting files (references, scripts, templates)
  principles/             the one implicitly invocable skill
    SKILL.md              index: how to use principles, then one line per principle with its condition
    <name>.md             a principle: a short rule that applies when its condition holds; no frontmatter
    agents/openai.yaml
scripts/
  check.py                validates the invariants below; run before every commit
  install.sh              symlinks skills into ~/.claude/skills and ~/.agents/skills
.claude/skills/           internal skills for maintaining this repo; not installed
.agents/skills/           project-local Codex links to the same internal skills
```

**Playbook or skill?** A playbook answers "what kind of task is this and what are the steps". A skill is a reusable capability that more than one playbook (or the user, directly) calls. Start new work as a playbook step. Extract a skill only when a second caller needs it. A principle is not a procedure. It is a rule with a condition ("when you measure, name the limiter") that any playbook or task can hit.

## Invariants

`python3 scripts/check.py` enforces these. Keep it passing.

- Every `skills/<name>/SKILL.md` has frontmatter `name: <name>` (matching the directory), a `description`, and `disable-model-invocation: true`. `principles` is the exception and must not set it.
- Every skill has `agents/openai.yaml` with `policy.allow_implicit_invocation: false`, except `principles`, which has `true`.
- Every file in `skills/yastack/playbooks/` is listed under **Playbooks** in `skills/yastack/SKILL.md` as `` - **Title** (`<name>`). <when> ``. Nothing listed is missing on disk.
- Every `skills/principles/<name>.md` is listed in `skills/principles/SKILL.md` as `` - [Title](<name>.md). <when> ``. Nothing listed is missing on disk.
- Every other skill is reachable: a relative link leads to it from the entry point, a playbook, or a file one of those links.
- Every relative link in a skill or playbook resolves to a file.

When you notice a new rule that keeps being broken, add it to `check.py` rather than to this file.

## How routing works

The two harness flags do different jobs:

- Claude Code `disable-model-invocation: true` keeps the skill's description out of the model's context and blocks the `Skill` tool from calling it. The user can still run `/<name>`.
- Codex `allow_implicit_invocation: false` keeps the skill out of the model's context. The user can still run `$<name>`.

Because the model can't invoke routed skills through the `Skill` tool, `yastack` loads them by path: playbooks at `playbooks/<name>.md` and skills at `../<name>/SKILL.md`, both relative to `skills/yastack/SKILL.md`. Principles live at `../principles/<name>.md`. Three things name a skill, and the agent reads its file only then: a non-negotiable in the entry point ("before commit → `unslop-code`"), a principle whose condition holds, or a playbook step. Every load stays visible in the transcript.

Subagents can't use slash commands. A brief that delegates a skill passes the skill file's absolute path and tells the subagent to read it.

The entry point is named after the stack. If yastack is ever packaged as a Claude Code plugin named `yastack`, `/yastack` still works: a bare name resolves to the plugin skill, and `/yastack:yastack` is only needed when another skill has the same name (tested on Claude Code 2.1.325).

## Changing the stack

Every change starts from evidence: a session where the stack did the wrong thing, did nothing, or made the user steer by hand. Write that evidence in the commit message: what was asked, what the agent did, what it should have done.

Adding or changing a skill or playbook:

1. Prefer editing an existing playbook or skill over adding a new one. A new file needs a second real use case, not a hypothetical one.
2. Write it tight. Keep only what the model would otherwise get wrong or do inconsistently: exact steps, gotchas, commands, output shapes. Cut general best practice, motivation, and padded examples.
3. For a skill: create `skills/<name>/SKILL.md` with the frontmatter above and `agents/openai.yaml` (copy one from an existing skill). Link it from the playbook step that uses it, or from a non-negotiable in `skills/yastack/SKILL.md` when it applies across tasks.
4. For a principle: create `skills/principles/<name>.md`, a `# Title` and the rule, with no frontmatter. Add `` - [Title](<name>.md). <applies when> `` under its group in `skills/principles/SKILL.md`. The entry states when it applies and the rule in one line. Link to it from elsewhere as `principles/<name>.md`.
5. For a playbook: create `skills/yastack/playbooks/<name>.md` and add `` - **Title** (`<name>`). <use for> `` under **Playbooks**.
6. Run `python3 scripts/check.py`. The pre-commit hook runs it again on commit.
7. Test it. Re-run the prompt from the original evidence in a fresh session, through `/yastack`, and confirm the route and the behavior changed. Say in the commit message whether you did this.

Removing is a feature. Suggest deleting a skill or playbook that hasn't been routed to in a while, or that a newer one supersedes.

Never bulk-import skill packs or generate batches of skills.

## Writing style for skills

- Address the agent in the second person and the imperative.
- Short declarative sentences. One instruction per sentence.
- Name exact files, commands, and output formats. "Run the tests" is weaker than the command.
- A `description` says what the skill does in one or two sentences. It is shown in the `/` menu, not used for triggering, so trigger phrases are not needed.

## Pre-commit is the only gate

There is no CI. The pre-commit hook (`.pre-commit-config.yaml`) is the only thing between a change and `main`, so every mechanical check and lint lives there:

- file hygiene: trailing whitespace, final newline, LF endings, YAML syntax, merge markers, shebangs and executable bits, private keys
- `ruff` lint and format for Python (`ruff.toml`)
- `shellcheck` for shell scripts
- `markdownlint-cli2` for Markdown (`.markdownlint-cli2.jsonc`)
- `scripts/check.py` for the stack invariants

Rules:

- Never commit with `--no-verify`, and never skip a hook with `SKIP=`. If a hook is wrong, fix the hook or its config in the same commit and say why in the message.
- A new kind of file or check gets its hook in the same change. If you add a language, add its linter.
- Some hooks fix files in place (whitespace, `ruff --fix`, `ruff format`). When the commit fails that way, review the fixes, `git add` them, and commit again.

## Commands

- `pre-commit install`: once per clone. Worktrees share the hook through the common git dir.
- `pre-commit run --all-files`: run every hook on the whole repo. Run it after changing a hook or a lint config.
- `pre-commit autoupdate`: bump the pinned hook revisions.
- `python3 scripts/check.py`: validate invariants only. Exits non-zero with one line per violation.
- `scripts/install.sh`: link every skill into `~/.claude/skills/` and `~/.agents/skills/`. Run from the main checkout, never from a worktree. Idempotent. `scripts/install.sh --uninstall` removes the links.
