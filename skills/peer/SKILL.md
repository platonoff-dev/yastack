---
name: peer
description: Run a brief on a model from another vendor, today OpenAI's through the Codex CLI, and report which model ran. Use when a step needs a judge, reviewer, or panel seat that is not Claude, or the user asks for a second opinion from another model.
---

# Peer

A peer is a model from another vendor, run headless through that vendor's CLI on the user's existing login. Today the only provider is Codex. A Claude judge scoring Claude candidates shares their blind spots. A peer doesn't.

`scripts/peer.py` picks the peer, so the vendor rule lives in code and not in each caller. It walks the preference order and skips Anthropic. It also skips any CLI that is missing or logged out. It runs the first one left. A failed run falls through to the next provider. Run the script by its path under the base directory the harness printed for this skill.

## Check what can run

```bash
python3 <base>/scripts/peer.py list
```

One line per provider, `ready` or `unavailable: <why>`. Run it when a peer failed and you need the reason, or when the user asks which peers work.

## Write the brief

A peer has no `Skill` tool, no yastack, no conversation history, and none of your context. It sees the brief and the files on disk.

- Write the brief to a file. Give it one task per run.
- Name every file it needs by absolute path. It can read anywhere. In read-only mode it can't write.
- Paste the rules it must follow. Where a subagent brief would name a principle or a skill, paste that rule's text instead.
- Mark the parts with XML tags. Use `<task>` for the job and its context. Use `<output_contract>` for the exact shape of the final message, since only the final message reaches `--out`. Use `<grounding_rules>` to say that every claim cites a file, a line, or command output, and that an inference is labeled as one.
- For a review or judge brief, add `<dig_deeper_nudge>`. It tells the peer to check second-order failures, empty states, retries, and stale state after the first issue it finds.
- For a write brief, add `<action_safety>`. It keeps edits inside the task, leaves them uncommitted, and allows no unrelated cleanup. Add `<verification_loop>` too, so the peer checks its result before it finishes. Its sandbox has no network, so tell it not to install packages.

## Run it

Read-only, for a judge or a reviewer:

```bash
python3 <base>/scripts/peer.py run --mode read-only --cwd <repo> --prompt-file <brief> --out <file>
```

Write, for a panel seat that edits code:

```bash
python3 <base>/scripts/peer.py run --mode write --worktree <new-path> --prompt-file <brief> --out <file>
```

`--worktree` creates a detached worktree at `HEAD` from the `--cwd` repo and copies in its uncommitted and untracked files. Write mode refuses any directory that isn't a linked worktree, so a peer never edits your checkout. Read the peer's edits with `git -C <new-path> status` and `git -C <new-path> diff`. Remove the worktree with `git worktree remove --force <new-path>` when the caller is done with it.

Run the command with `Bash` and `run_in_background: true`. A run takes minutes, and a foreground `Bash` call stops at 10. In a fan-out, send it in the same message as the `Agent` calls, so it runs alongside them. You are re-invoked when it exits. `--timeout` (default 1500 seconds) covers every attempt together and stays under the 30-minute background default. Raise the `Bash` `timeout` with it.

`--provider <name>` runs only that provider, for a user who asked for one by name.

## Read the result

On success the last stdout line is `peer provider=<name> vendor=<vendor> model=<id> cwd=<dir> out=<file>`. Stderr has one `peer: skip <name>: <why>` line per provider that didn't run.

- **Exit 0.** Read `--out`. Credit the work as `<model> (<vendor>)` wherever the caller reports who ran it, such as `reviewed by`.
- **Exit 3.** No peer could run. Do the step with a native `Agent` subagent instead. In the reply, say that no peer ran and quote the skip lines.
- **Exit 4.** A write run failed after editing its worktree. The script stops there rather than run another peer on half-done edits. Treat the seat as a dropout and keep the worktree for inspection.

You own a peer's output like any subagent's. Verify a claim before acting on it, and write your own summary. Never paste the output through as your answer.

## Configure

`providers.toml` next to this file holds the providers and how to run each one. Your model and effort choices, and the `order` list once there are several providers, go in `~/.config/yastack/peers.toml`, outside the repo:

```toml
[codex]
model = "<model id>"
effort = "xhigh"
```

Leave a model unset to use the CLI's own default. To add a provider, add an entry to `providers.toml` with the fields its header lists. Then run it once in each mode with `--provider <name>` before you commit it.
