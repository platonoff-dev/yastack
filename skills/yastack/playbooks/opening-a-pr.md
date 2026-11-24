# Opening a PR

Invoked at the end of every other playbook.

Use this playbook to open, update, or stack a change request: a GitHub pull request or a GitLab merge request. "PR" below means either. "Base" means the branch the PR merges into, which GitLab calls the target branch.

**Worktree.** Work from a git worktree off main. Pass its path to subagents. Multiple subagent calls on the same branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Dirty branch with unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally.

**Commits.** Commit liberally. Rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit. New commit when separable. Commit bodies don't restate the subject.

**PRs.** Load and run the `unslop-code` skill over the diff before commit and the `unslop-comments` skill before review. Write every PR title, description, and commit body with the `technical-writing` skill (every layer except Diátaxis, and apply the STE vocabulary rules: one word per action, keep articles, a plain verb over `-ing` where one works), then load and apply the `unslop-prose` skill.

**Review before push.** Run this loop before every push of a branch, including the push that opens or updates a PR or goes straight to a remote branch. Commit the work first. Keep unrelated edits out of the commit. In this loop, `<branch>` is the branch you push, and the checkout is the worktree where it is checked out. `<base>` is the fetched remote ref the push is compared against. For a PR branch, it is the PR base on the remote the PR targets, such as `origin/main` or the parent branch in a stack. For a direct push to an existing remote branch, it is that remote branch. For a new branch without a PR, it is the remote branch it was cut from. Run `git fetch <remote>` for the remote that holds `<base>`. Name `<branch>` in every range, not `HEAD`, because the `code-review` skill runs in the session's working directory, which may not be the checkout. Give every `Agent` seat the checkout's absolute path. Tell it to run every read and command there. Tell it to ignore changes outside `<base>...<branch>`. Do not edit the checkout until every seat in the round returns, because the peer review reads its working tree.

1. Load the `peer` skill with `Skill`. Then start three fresh reviewers in one message. None of them edits files.
   - Correctness seat. A general-purpose `Agent` subagent. Tell it to load the `code-review` skill with `Skill` and run it with the args `high <base>...<branch>`, without `--fix` or `--comment`.
   - Peer seat. Run the `peer` skill's branch review in the background. Pass `<base>` as `--base` and the checkout as `--cwd`. Write `--out` outside the checkout. If no peer can run, start a second correctness seat instead and say in the reply that no peer ran.
   - Scope seat. A general-purpose `Agent` subagent. Its brief holds the task as the user gave it, every later directive verbatim, the planned scope of this PR when the task spans a stack, the command `git diff <base>...<branch>`, and the scope checklist below. Tell it to load the `principles` skill with `Skill` and read the `test-behavior-not-implementation` principle.
2. Tell each `Agent` seat to return one line per finding as `file:line`, the claim, and the evidence or the failure scenario, or the single line `no findings`. Each seat also states the range it reviewed and its commit count. A seat that could not review that range does not count. Run it again once. If it fails again, do not push. Tell the user which seat failed and why.
3. Triage every finding yourself. Verify it against the code or a run before you act on it. Fix each real finding. Rerun the checks it touches. Commit the fix. Dismiss the rest with a concrete reason.
4. Run the next round with fresh seats. Give the correctness and scope seats each dismissed finding with its reason, and tell them to raise it again only with new evidence. The peer review takes no instructions, so a finding it repeats without new evidence stays dismissed.
5. Stop when every seat in one round returns no finding you accept. Then push. After three rounds without that, do not push. Show the user the open findings with your reasons and ask.

Scope checklist:

- Every change traces to the task. An unrequested change passes only when the task clearly missed a detail that the change needs. Name that detail.
- Every part of the task, or of this PR's planned scope in a stack, is done.
- No scope creep, such as unrequested refactors, renames, reformatting, drive-by cleanups, new dependencies, new flags or config, or an abstraction with one caller.
- Tests check behavior, not implementation. Flag tests that restate the code, mock the unit under test, repeat cases, or outweigh the change.
- Comments explain only a non-obvious why. Flag comments that narrate the code, log the change ("now uses X"), or refer to the task or the review.
- Flag defensive code for impossible states, swallowed errors, weakened or skipped tests, and silenced lint or type checks.
- Flag debug output, dead code, new TODOs, and stray files.

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

A subagent that opens a PR loads and runs the `unslop-code` and `unslop-comments` skills. It returns to the parent without babysitting. With the `Agent` tool, it runs the review loop, pushes, opens the PR, and posts the URL. Its brief carries the user's task and every later directive verbatim, for the scope seat. Without it, the subagent commits, does not push, and returns its worktree, branch, and base. The parent then runs the loop, pushes, opens the PR, and posts the URL.

## Forge commands

| action | GitHub (`gh`) | GitLab (`glab`) |
| --- | --- | --- |
| create | `gh pr create --title "<title>" --body-file <file>` | `glab mr create --title "<title>" --description-file <file> --yes` |
| create on a base | add `--base <branch>` | add `--target-branch <branch>` |
| mark ready | `gh pr ready <number>` | `glab mr update <number> --ready` |
| view | `gh pr view <number>` | `glab mr view <number>` |
| retarget | `gh pr edit <number> --base <branch>` | `glab mr update <number> --target-branch <branch>` |
