# Opening a PR

Use this playbook to open, update, or stack a change request: a GitHub pull request or a GitLab merge request. "PR" below means either. "Base" means the branch the PR merges into, which GitLab calls the target branch.

1. **Resolve the forge.** Run `git remote get-url origin`. A `github.com` remote uses `gh`. Otherwise, if `glab repo view` succeeds, use `glab`, which also covers self-hosted GitLab. If neither works, ask the user. Use only that forge's commands from the table below for the rest of the task.
2. **Branch.** Work on a branch from an up-to-date default branch, never on the default branch itself. If the branch carries unrelated work, move that work to its own branch first.
3. **Clean the code.** Read [unslop-code](../../unslop-code/SKILL.md) in full and apply it to the diff. Then read [unslop-comments](../../unslop-comments/SKILL.md) and run it.
4. **Shape the commits.** Before the first push, rebase into small, ordered commits. Each commit lands on its own, and the order tells the story. Amend when a fix belongs in the commit you just made. Make a new commit when the fix is separable. After the first push, add commits instead of rewriting, unless the user asks.
5. **Write the title.** Run `git log --oneline -20` and match the repo's convention, such as a ticket key prefix. With no convention, use Conventional Commits: `type(scope): subject`, with no trailing period. The type is `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf`. The scope is the area of the code. The subject is short and imperative, and names the real symbol when one carries the change.
6. **Write the description.** Read [technical-writing](../../technical-writing/SKILL.md) and apply every layer except Diátaxis. It ends with `unslop-prose`. The body is a one-minute briefing for a reviewer who has the diff. It can become the squash commit body, so keep it under about 40 lines. If the repo has a PR or MR template, fill it in instead of the headings below. Otherwise use these `##` headings in this order, and drop a section that has nothing to say, except Scope:
   - `## Why`: the problem and the approach, in one to three sentences.
   - `## What changed`: one to three bullets. Name a symbol or path only when it carries the change. Name both sides of a rename.
   - `## Scope`: always present. What the change covers and what it leaves out, such as a follow-up or a known gap.
   - `## Tradeoffs`: only the rejected alternatives a reviewer would ask about.
   - `## Blast radius`: who or what the change touches, and why that is safe or risky.
   - `## Verification`: one to three bullets, each a command or run path and its result. For performance, give one number with its unit as `before → after`.

   Leave out SHAs, rebase history, file-by-file lists, and logs. Attach a screenshot or video only when it proves a claim.
7. **Open it ready.** Write the body to a file, then run the create command without the draft flag. If the PR still opens as a draft, run the mark-ready command. Run the view command before you state the status of a PR. Post the URL.
8. **Stack when it is large.** Prefer several narrow PRs to one large PR. Each child branch starts at its parent's tip, and its PR uses the parent branch as its base. When a parent merges, rebase the child onto the default branch, then view the child PR. If its base is still the merged branch, retarget it to the default branch. Branch from the default branch only for independent work.
9. **Don't babysit.** Opening a PR doesn't start a watch on CI or reviews. Post the URL and keep working until the whole stack exists. Watch CI and reviews only when the user asks. A subagent that opens a PR posts the URL and returns.

## Forge commands

| action | GitHub (`gh`) | GitLab (`glab`) |
| --- | --- | --- |
| create | `gh pr create --title "<title>" --body-file <file>` | `glab mr create --title "<title>" --description-file <file> --yes` |
| create on a base | add `--base <branch>` | add `--target-branch <branch>` |
| mark ready | `gh pr ready <number>` | `glab mr update <number> --ready` |
| view | `gh pr view <number>` | `glab mr view <number>` |
| retarget | `gh pr edit <number> --base <branch>` | `glab mr update <number> --target-branch <branch>` |
