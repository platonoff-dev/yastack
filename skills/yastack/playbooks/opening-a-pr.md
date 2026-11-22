# Opening a PR

Invoked at the end of every other playbook.

Use this playbook to open, update, or stack a change request: a GitHub pull request or a GitLab merge request. "PR" below means either. "Base" means the branch the PR merges into, which GitLab calls the target branch.

**Worktree.** Work from a git worktree off main. Pass its path to subagents. Multiple subagent calls on the same branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Dirty branch with unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally.

**Commits.** Commit liberally. Rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit. New commit when separable. Commit bodies don't restate the subject.

**PRs.** Load and run the `unslop-code` skill over the diff before commit and the `unslop-comments` skill before review. Write every PR title, description, and commit body with the `technical-writing` skill (every layer except Diátaxis, and apply the STE vocabulary rules: one word per action, keep articles, a plain verb over `-ing` where one works), then load and apply the `unslop-prose` skill.

**Titles.** Conventional Commits `type(scope): subject`, no trailing period. Type such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf`. Scope is the area, such as `yastack`. Subject is short, imperative, and names a real symbol when one carries the change, for example `fix(yastack): retarget opening-a-pr babysit trigger`.

**Descriptions.** The PR body is a one-minute briefing, not a lab notebook, for a reviewer who has the diff. It says why the change exists, what it leaves out, what it could break, and how you proved it works. Write short, simple sentences with few identifiers, no walls of text. The body becomes the squash commit body, so keep that commit under about 40 lines. Use `##` headings, not bold lead-ins, in this order, and drop a section with nothing to say:

- `## Why`: the problem and approach, 1–3 short sentences. No SHAs, rebase genealogy, or "based on main" preamble.
- `## What changed`: 1–3 short bullets. Name a real symbol or path only when it carries the change. Name both sides of a rename or retarget.
- `## Scope`: always. 1–3 short items on what it covers and what it deliberately leaves out (a follow-up, a known gap). No symbols, paths, or file-by-file essay.
- `## Tradeoffs`: only rejected alternatives a reviewer would otherwise ask about. Skip when there was no real choice.
- `## Blast Radius`: 1–2 sentences on who or what it touches and why that is safe or risky. If main is red, state the cost of leaving it red.
- `## Verification`: 1–3 bullets, each a real run path and its outcome. Perf: one primary number with its unit, `before → after`, and a link to an artifact for the rest. No sample-size methodology, subagent recitals, or metric tables.

After the sections, attach videos or screenshots when they prove a claim. Full SHAs, subagent recitals, lever-correction essays, file-by-file checklists, and "CLEAN" verdicts go in a linked artifact, not the body.

**Forge.** Resolve the forge before the first PR operation and keep that choice for create, edit, view, watch, and merge. Run `git remote get-url origin`. A `github.com` remote uses `gh`. Otherwise, if `glab repo view` succeeds, use `glab`, which also covers self-hosted GitLab. If neither works, ask the user. Use the resolved forge's commands from the table below when no built-in PR tool covers the operation.

**Built-in PR tool.** When the run provides a built-in PR tool for the resolved forge, create, edit, retarget, and mark ready through it, never through a forge CLI. A CLI-made PR misses what the tool tracks. Use the resolved forge for everything the tool does not cover, and for every PR operation when the run has no such tool.

**Size and stacks.** Prefer five narrow PRs to one large PR. A stack is a base-branch chain. The root PR targets trunk. Each child branch rebases onto its parent's exact tip and its PR targets the parent branch. As a parent merges, rebase its child onto trunk, then view the child PR. If its base is still the merged branch, retarget it to trunk. Without a built-in PR tool, use the resolved forge's create-on-a-base and retarget commands from the table below. Branch from trunk only for independent work. Rebase on trunk before substantial stack work.

**Readiness.** Open every PR ready, never as a draft. A built-in PR tool can default to draft, so set `draft: false` on every creation call through it. With `gh` or `glab`, omit `--draft`. If a PR still opens as a draft, mark it ready through the PR tool, or run the mark-ready command according to the resolved forge. Run the resolved forge's view command before you refer to PR status.

**Babysit.** Opening a PR does not start a babysit. Post the URL and keep building. Finish the phase or stack first. Run a separate babysit pass only when the user asks for one after the whole stack exists. A babysit for each new PR stalls the build and spends checks on commits later waves restart. Push back when feedback drifts from intent.

A subagent that opens a PR loads and runs the `unslop-code` and `unslop-comments` skills, and posts the URL. It returns to the parent without babysitting.

## Forge commands

| action | GitHub (`gh`) | GitLab (`glab`) |
| --- | --- | --- |
| create | `gh pr create --title "<title>" --body-file <file>` | `glab mr create --title "<title>" --description-file <file> --yes` |
| create on a base | add `--base <branch>` | add `--target-branch <branch>` |
| mark ready | `gh pr ready <number>` | `glab mr update <number> --ready` |
| view | `gh pr view <number>` | `glab mr view <number>` |
| retarget | `gh pr edit <number> --base <branch>` | `glab mr update <number> --target-branch <branch>` |
