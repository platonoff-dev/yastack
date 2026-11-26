---
name: unslop-code
description: Remove AI-generated code slop and clean up code style
---

# Remove AI code slop

Check the diff against the base branch, default `main`, including uncommitted changes, and remove AI-generated slop introduced in it.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Type-checker or linter escapes used only to bypass type or lint issues
- Deeply nested code that should be simplified with early returns
- Judge new code against these rules, not existing slop in the surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences), and name any bug fix that changed behavior.
