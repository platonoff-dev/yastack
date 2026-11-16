---
name: technical-writing
description: Layered technical-writing standard (Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax) for docs, READMEs, PR descriptions, and commit messages.
disable-model-invocation: true
---

# Technical writing

Write so a tired engineer understands on the first read. Apply all four layers, then apply [unslop-prose](../unslop-prose/SKILL.md), which owns the catalog of AI tells.

Three rules sit above the layers:

- **Cut every word that does no work.** If the sentence survives without a word, the word goes.
- **Use the short, everyday word.** A long word has to buy its length with precision.
- **When a rule makes a sentence worse, fix the sentence another way or leave it alone.** A sentence that follows every rule and sounds like a machine wrote it has failed.

The codebase is the word list. Write the real symbol, file, flag, or command name, not a synonym or a description of it. A named pattern is fine when the doc says what it means the first time.

## Vary the rhythm

A doc can obey every layer and still read machine-written: every sentence clipped short, no view anywhere, nothing specific.

- Mix sentence lengths on purpose. Short sentences land a point. Longer ones carry a fact with its condition or consequence.
- Split the sentence that carries two thoughts. Keep the long sentence that carries one.
- Have a view where the mode allows it. Explanation weighs trade-offs, so say what you make of them instead of listing pros and cons. Reference stays dry.
- Be specific over sterile. Not "schema changes can cause issues" but "a column rename fails the build".

## Pick the mode first (Diátaxis)

One document, one mode. Two questions pick it: does the content inform action (doing) or understanding (thinking), and does it serve learning or work?

- Action + learning: **tutorial**.
- Action + work: **how-to**.
- Understanding + work: **reference**.
- Understanding + learning: **explanation**.

**Tutorial: learning by doing.** The learner's success is your job, not theirs. Open by saying what the learner will build, not what they will "learn". Every step produces a visible result, early and often. Tell them what they should see: the expected output, the prompt change, the log line. Cut explanation to one clause and a link. Write as "we", in commands: "First, do x. Now, do y."

**How-to: steps to a goal.** Solve a problem a person has, not an operation the machine can perform. Assume competence and skip teaching. Action only: no digressions, no background, no completeness for its own sake. Link those instead. Allow forks: "If you want x, do y." Name the guide by the task: "How to rotate the signing key", not "Signing key rotation".

**Reference: facts for lookup.** Only describe. No instruction, no persuasion, no opinion. State facts, options, limits, and errors with no hedging. Mirror the structure of the thing described, so code and docs can be navigated together. Generate from code where possible.

**Explanation: understanding and why.** One bounded topic, readable away from the product. Each title should tolerate an implicit "About..." in front. Anchor on a real why question. Give context: design decisions, history, constraints, alternatives. Opinion is allowed here and nowhere else.

Don't mix modes: no reference tables inside a tutorial, no tutorial hand-holding inside reference, no arguing inside a how-to. Split and link instead.

## Write sentences to the reader (Google developer style)

- Talk to the reader as "you", in the present tense. Use "will" only for things that happen later.
- Write instructions as commands: "Run `make test`." State facts plainly. Never "should be done".
- Put the condition before the instruction: "To delete the branch, run `git branch -D`."
- Put the common case first. Exceptions after.
- No "please" in instructions, and never "simply", "easy", or "quickly" in a procedure. If it were simple, the reader would not be here.
- Don't pre-announce ("we will soon support...") and don't start consecutive sentences with the same phrase.
- Link with words that say where the link goes: the page title or a short description. Never "click here".
- Headings carry the point, not just the topic ("Pick the mode first", not "Modes"). A task heading is a bare verb phrase ("Create an instance"). A concept heading is a noun phrase. One h1 per page, no skipped levels.
- Numbered lists for sequences, bullets for everything else. Introduce a list with a complete sentence. Keep items parallel.
- Code goes in code font. UI elements go in bold. Use serial commas. Drop "etc." and say up front that a list is partial.

## Make statements load one at a time (STE rules)

- One instruction per sentence. One thought per sentence everywhere else.
- Split instructions longer than about 20 words and other sentences longer than about 25.
- Put the warning or condition before the step it guards.
- Keep "the" and "a": "Remove backup file" reads two ways. "Remove the backup file" reads one.
- Give each word one meaning and one job. If "check" means inspect, don't also use it for restrain.
- Pick one word per action and stick to it: "start", not "start" here and "initiate" there.
- Write procedures as direct commands, never as narration and never in the passive: "Install the component", not "the component must be installed".
- Avoid "-ing" words where a plain verb works.

## Leave no sentence open to two readings (Global English)

- Keep words like "only" and "not" next to the word they change: "only fails on growth" and "fails only on growth" say different things.
- Break up long noun strings: "the skill invariant check script" becomes "the script that checks the skill invariants".
- Make every "it", "they", and "this" point at one obvious thing. Repeat the noun when in doubt. Never use "this" or "which" to point at a whole clause.
- Don't drop verbs: "Phase 1 moves the converters and Phase 2 the runtime" leaves Phase 2 without one.
- Keep the small words that show structure, such as "that" in "Ensure that the switch is off".
- Repeat the article in a series when it prevents a misread: "the client and the host", not "the client and host", when they are two things.
- Say which parts "and" or "or" joins when a sentence can group two ways. "Both...and", "either...or", and "if...then" disambiguate for free.
- Use periods, not semicolons.
- Make text in parentheses a full grammatical unit or its own sentence. Never form plurals with "(s)".
- No slashes: write "a, b, or both" instead of "a/b" or "and/or".
- Call each thing by one name, everywhere. Don't churn what didn't change.
- Skip idioms, colloquialisms, and Latin abbreviations.

## PR descriptions and commit messages

Every layer except Diátaxis applies to them. A PR body is a briefing that a reviewer can read in under a minute. Don't paste logs, SHA lists, or metric tables. Link them. Write real paths. Make every count or tree claim true at the commit that lands it, and include the command that regenerates it.

## Worked example

Before:

> Validation of the skill invariants is performed by the check script. It's important to note that running it should be done before every commit, and if any violations are found, the commit will be blocked by the hook.

After:

> `scripts/check.py` checks the stack invariants and prints one line per violation. The pre-commit hook runs it, so a violation blocks the commit.
