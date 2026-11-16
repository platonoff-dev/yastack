---
name: unslop-code
description: Remove AI-generated slop from the code a branch adds, such as narrating comments, needless defensive code, type-checker escapes, and deep nesting.
disable-model-invocation: true
---

# Unslop code

Remove the slop this branch added. Edit only lines in the diff.

## Scope

Use the files or diff the caller names. Otherwise use `git diff $(git merge-base HEAD main)`, which includes uncommitted changes, plus the untracked files in `git status --short`.

## Cut

- Comments that narrate the next line, restate a name, or log the change ("added X", "now uses Y").
- Defensive checks, fallbacks, and `try`/`catch` or `try`/`except` blocks on paths whose input is already trusted or validated. Keep checks at real boundaries: user input, network, files, and other processes.
- Escapes that only silence the type checker or linter: casts to an untyped top type (`any`, `object`, `interface{}`), `# type: ignore`, `@ts-ignore`, `# noqa`, `//nolint`, and unchecked non-null assertions. Fix the type or the code instead. If the escape is truly needed, keep it with the rule name and the reason.
- Deep nesting that early returns would flatten.
- Code nothing calls: unused parameters, helpers, and flags, and compatibility paths for callers that don't exist.

## Don't copy existing slop

Judge the new code against the list above, not against the code around it. The surrounding code can be slop too, and a pattern that appears there is no reason to keep it in the diff. Match the file only for naming, layout, and error-handling conventions. Leave slop outside the diff alone, and name it in one line if it deserves a follow-up.

## Guardrails

- Keep behavior unchanged unless you fix a clear bug. Name the bug in your summary.
- Make small, focused edits. Don't rewrite code outside the diff.
- Run the repo's tests and linters for the touched files.
- End with a summary of one to three sentences.
