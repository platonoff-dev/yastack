---
name: unslop-comments
description: Spawn a subagent with fresh context to delete excess comments from a diff, then review what it deleted.
disable-model-invocation: true
---

# Unslop comments

The agent that wrote the code defends its own comments. Don't do this pass yourself. Hand it to a subagent that has not seen the session.

## Scope

Use the files or diff the caller names. Otherwise use `git diff $(git merge-base HEAD main)`, which includes uncommitted changes, plus the untracked files in `git status --short`.

## Steps

1. Spawn one subagent with fresh context: `Agent` with `subagent_type: general-purpose` in Claude Code, `spawn_agent` in Codex. Its prompt is the brief below, verbatim except that `<why-skill>` becomes the absolute path of the [why](../why/SKILL.md) skill, then the scope. If you have no subagent tool, run the brief yourself as a separate pass over the diff only.
2. Review its diff. Revert every edit to code that is not a comment, every edit outside the scope, and every deletion of a comment that fits a keep rule. Before accepting thin `IMPORTANT` or `do not remove` deletions or keeps, trace their symbol or run the [why](../why/SKILL.md) skill on it. If a deletion is ambiguous, do not restore it. If a keep is refuted or still ambiguous, delete it. If you reject most of the report, run the subagent once more with the failure named.
3. Act on each `RESHAPE` flag inside the scope with the smallest fix: a rename, an extracted function, a type, or the real API. Report flags you can't fix in scope as open. Never restore the deleted comment.
4. A comment that says `do not remove`, `do not change`, or `talk to X first` about our own code is an untested constraint. Offer the cheapest test, type, or lint check that enforces it, and wait for the user. If they agree, add the check, then delete the comment. Otherwise delete it and report the constraint as open.
5. Report the deletion count, `RESHAPE` fixes, `REVIEW` keeps, reverted deletions, and open items.

## Brief

```text
Delete excess comments in the scope below. Edit comments only. Never change code.

Keep only these comments:
- License or legal headers.
- Comments on behavior forced by an external dependency, platform, vendor, or protocol that we cannot change.
- Doc comments that define a public API contract.
- Lint or type suppressions whose rule is wrong, pedantic, or style-only for that line.
- Issue or RFC links that explain a constraint the code cannot express.

Delete everything else: narration, banners, commented-out code, change history, and justifications for workarounds. If you are not sure a keep rule applies, delete the comment.

If a comment explains a surprise in our own code, delete it. Flag the symbol as RESHAPE and name the rename, extraction, or type that makes the comment unnecessary.

If a suppression hides a rule that catches real bugs or guards safety, delete it and flag the symbol as RESHAPE.

If a comment claims a rule of an external dependency, check that dependency's docs or source. Delete the comment only if the claim is false or the rule doesn't apply to us. If you can't check, keep it and list it under REVIEW with the rule it claims, quoted word for word.

IMPORTANT, "do not remove", "too risky", and "fine for now" are not proof. Before you judge such a comment, read the nearby code. If its claim is not obvious there, trace the named symbol or call with `git log -S '<symbol>'` and `git blame`, run the why skill at <why-skill> on it, or both.

Flag only problems the code has today. Invent nothing.

Report the files you touched, the deletion count, each RESHAPE flag in one line, and each REVIEW keep with the rule it claims.
```
