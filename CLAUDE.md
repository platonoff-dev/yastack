# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this repo is

yastack is a personal stack of agent skills for Claude Code, and only Claude Code. pstack is tuned to Cursor and names Cursor tools. yastack is tuned to Claude Code the same way: skills name Claude Code tools, parameters, and features directly, such as `Agent`, `AskUserQuestion`, `isolation: "worktree"`, and `disable-model-invocation`. Do not add a portability layer or instructions for another harness. It borrows three ideas from poteto's pstack and nothing else by default:

1. **One entry point.** The user types `/yastack <task>` and the stack decides which playbook and skills apply. The user never has to remember which skill fits which task.
2. **Explicit routing.** A route names the skill a step needs, and the agent loads it with the `Skill` tool at that step. Only the entry point sets `disable-model-invocation: true`, so `/yastack` stays a user command. Every other skill stays model-invocable, because the `Skill` tool refuses a skill with that flag and tells the agent not to replicate it by other means.
3. **Principles.** Short rules that cut across playbooks, such as "explain the number before you trust it". They are plain Markdown files under one skill, `principles`, whose `SKILL.md` indexes each one with the condition it applies under. The model can load the index for any task, not only under `/yastack`. The entry point loads it at the start of every task. The agent reads a principle file when its condition holds or the user names it, and names it in the final reply.

The stack grows by iteration on real use. A skill or playbook earns its place by fixing something that went wrong in an actual session. Skills may be adopted from pstack or elsewhere, but each one is judged first. For pstack, follow `.claude/skills/adopt-skill/SKILL.md`. Keep the source text as close to the original as possible. Reject unmet required dependencies rather than deleting the steps that need them.

The remote is public (`github.com/platonoff-dev/yastack`). Nothing work-specific goes here: no employer systems, people, tickets, hostnames, or secrets. Work skills live in the separate corporate `dotai` repo.

## Layout

```text
skills/
  yastack/                entry point (the router)
    SKILL.md              modeled on pstack's poteto-mode: non-negotiables, principles, autonomy,
                          subagents, reply and comment rules, the playbook list
    playbooks/<name>.md   one procedure per task kind (bug fix, feature, ...)
  <name>/                 a routed skill: a capability that playbooks call
    SKILL.md
    ...                   supporting files (references, scripts, templates)
  principles/             the principles index
    SKILL.md              index: how to use principles, then one line per principle with its condition
    <name>.md             a principle: a short rule that applies when its condition holds; no frontmatter
scripts/
  check.py                validates the invariants below; run before every commit
  install.sh              symlinks skills into ~/.claude/skills
.claude/skills/           internal skills for maintaining this repo; not installed
```

**Playbook or skill?** A playbook answers "what kind of task is this and what are the steps". A skill is a reusable capability that more than one playbook (or the user, directly) calls. Start new work as a playbook step. Extract a skill only when a second caller needs it. A principle is not a procedure. It is a rule with a condition ("when you measure, name the limiter") that any playbook or task can hit.

## Invariants

`python3 scripts/check.py` enforces these. Keep it passing.

- Every `skills/<name>/SKILL.md` has frontmatter `name: <name>` (matching the directory) and a `description`. `yastack` sets `disable-model-invocation: true`. No other skill sets it.
- Every file in `skills/yastack/playbooks/` is listed under **Playbooks** in `skills/yastack/SKILL.md` as `` - **Title** (`<name>`). <when> ``. Nothing listed is missing on disk.
- Every `skills/principles/<name>.md` is listed in `skills/principles/SKILL.md` as `` - [Title](<name>.md). <when> ``. Nothing listed is missing on disk.
- Every other skill is reachable: the entry point, a playbook, or a skill one of those names refers to it as `` `<name>` ``.
- Every relative link in a skill or playbook resolves to a file inside the same skill's directory. Refer to a skill as the `` `<name>` `` skill and to a principle as the `` `<name>` `` principle. No skill outside `yastack` refers to a playbook.
- Every `` `<name>` `` principle names a file in `skills/principles/`. A skill that names one also names the `principles` skill.
- No skill mentions Codex or ships `agents/openai.yaml`. yastack targets Claude Code only.

When you notice a new rule that keeps being broken, add it to `check.py` rather than to this file.

## How routing works

**Load skills with the `Skill` tool, never as files.** When a skill, playbook, or principle sends the agent to another skill, write "the `` `<name>` `` skill". At a step that runs it, also write "load it with `Skill`". Without those words, a skill run outside `/yastack` reads the other skill's file with `cat` (seen in a headless `/architect` run). Never link to its `SKILL.md`, give its path, or tell the agent or a subagent to read it. A file read skips the harness's skill loading, and a skill locked with `disable-model-invocation: true` makes the `Skill` tool refuse and tell the agent not to replicate it by other means. `scripts/check.py` rejects cross-skill `SKILL.md` links and paths.

`disable-model-invocation: true` keeps the skill's description out of the model's context and blocks the `Skill` tool from calling it. The user can still run `/<name>`. Only `yastack` sets it.

Three things name a skill, and the agent loads it only then: a non-negotiable in the entry point ("before commit → `unslop-code`"), a principle whose condition holds, or a playbook step. Every load stays visible in the transcript.

**Never reach into another skill's directory by path.** A relative path resolves only against the base directory the harness prints for the skill it just loaded. A path into a sibling skill works only by accident of the install layout, and the agent can resolve it against the working directory instead. So:

- **Principles** are files inside the `principles` skill. Everywhere else, name one as "the `` `<name>` `` principle". The agent loads the `principles` skill with `Skill`, and the index links each file relative to its own base directory. Links between principle files stay inside that skill and are fine.
- **Playbooks** are files inside `yastack`, read only after `/yastack` loads it: `playbooks/<name>.md` relative to its base directory. Playbooks link each other and `../SKILL.md` freely. No other skill refers to a playbook, because outside `/yastack` the agent has no way to locate one. Put the rule a skill needs in the skill itself, or in the playbook that calls the skill.

Subagents spawned with `Agent` can't use slash commands, but they have the `Skill` tool. A brief that delegates a skill names it and tells the subagent to load it with `Skill`. A brief names each principle the subagent needs and tells it to load the `principles` skill with `Skill`. A brief passes an absolute path only for a playbook or a reference file. A subagent that loads a fan-out skill (`arena`, `architect`, `interrogate`) as context is one worker in it. Its brief names that role and tells it not to fan out again.

The entry point is named after the stack. If yastack is ever packaged as a Claude Code plugin named `yastack`, `/yastack` still works: a bare name resolves to the plugin skill, and `/yastack:yastack` is only needed when another skill has the same name (tested on Claude Code 2.1.325).

## Changing the stack

Every change starts from evidence: a session where the stack did the wrong thing, did nothing, or made the user steer by hand. Write that evidence in the commit message: what was asked, what the agent did, what it should have done.

Adding or changing a skill or playbook:

1. Prefer editing an existing playbook or skill over adding a new one. A new file needs a second real use case, not a hypothetical one.
2. Write it tight. Keep only what the model would otherwise get wrong or do inconsistently: exact steps, gotchas, commands, output shapes. Cut general best practice, motivation, and padded examples.
3. For a skill: create `skills/<name>/SKILL.md` with the frontmatter above. Name it as the `` `<name>` `` skill from the playbook step that uses it, or from a non-negotiable in `skills/yastack/SKILL.md` when it applies across tasks.
4. For a principle: create `skills/principles/<name>.md`, a `# Title` and the rule, with no frontmatter. Add `` - [Title](<name>.md). <applies when> `` under its group in `skills/principles/SKILL.md`. The entry states when it applies and the rule in one line. Elsewhere, name it as the `` `<name>` `` principle, never as a link or path.
5. For a playbook: create `skills/yastack/playbooks/<name>.md` and add `` - **Title** (`<name>`). <use for> `` under **Playbooks**.
6. Run `python3 scripts/check.py`. The pre-commit hook runs it again on commit.
7. Test it. Re-run the prompt from the original evidence in a fresh session, through `/yastack`, and confirm the route and the behavior changed. Say in the commit message whether you did this.

Removing is a feature. Suggest deleting a skill or playbook that hasn't been routed to in a while, or that a newer one supersedes.

Never bulk-import skill packs or generate batches of skills.

## Writing style for skills

- Address the agent in the second person and the imperative.
- Short declarative sentences. One instruction per sentence.
- Name exact files, commands, and output formats. "Run the tests" is weaker than the command.
- A `description` says what the skill does in one or two sentences. It sits in every session's skill list, so keep it short.

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
- `scripts/install.sh`: link every skill into `~/.claude/skills/`. Run from the main checkout, never from a worktree. Idempotent. `scripts/install.sh --uninstall` removes the links.
