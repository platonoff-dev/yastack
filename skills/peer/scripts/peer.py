#!/usr/bin/env python3
"""Run a brief on a model from another vendor through that vendor's CLI. See ../SKILL.md."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
import tomllib
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REGISTRY = SKILL / "providers.toml"
LOCAL = Path(os.environ.get("YASTACK_PEERS", Path.home() / ".config" / "yastack" / "peers.toml"))
PARENT_VENDOR = "anthropic"
NO_PEER = 3
DIRTY_FAILURE = 4
PLACEHOLDER = re.compile(r"\{(\w+)\}")


class Unavailable(Exception):
    pass


def log(msg):
    print(f"peer: {msg}", file=sys.stderr)


def load():
    registry = tomllib.loads(REGISTRY.read_text())
    local = tomllib.loads(LOCAL.read_text()) if LOCAL.is_file() else {}
    providers = registry["provider"]
    for name, override in local.items():
        if isinstance(override, dict):
            if name not in providers:
                sys.exit(f"peer: {LOCAL} configures unknown provider {name!r}")
            providers[name] = providers[name] | override
    return local.get("order", registry["order"]), providers


def git(cwd, *args, **kw):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, check=True, **kw)


def git_state(cwd):
    status = git(cwd, "status", "--porcelain=v1", "-uall").stdout
    return status + git(cwd, "diff", "HEAD", "--binary").stdout


def make_worktree(source, path):
    """Detached worktree at HEAD with the source's uncommitted and untracked files carried over."""
    if path.exists():
        sys.exit(f"peer: {path} already exists; pass a new path to --worktree")
    root = Path(git(source, "rev-parse", "--show-toplevel", text=True).stdout.strip())
    git(root, "worktree", "add", "--detach", str(path), "HEAD")
    patch = git(root, "diff", "HEAD", "--binary").stdout
    if patch:
        subprocess.run(["git", "-C", str(path), "apply", "--binary"], input=patch, check=True)
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z", text=True).stdout
    for rel in filter(None, untracked.split("\0")):
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, path / rel)
    return path


def is_linked_worktree(cwd):
    try:
        dirs = git(cwd, "rev-parse", "--absolute-git-dir", "--git-common-dir", text=True).stdout
    except subprocess.CalledProcessError:
        return False
    git_dir, common = dirs.split()
    return Path(git_dir).resolve() != (Path(cwd) / common).resolve()


def check(provider):
    if provider["vendor"] == PARENT_VENDOR:
        raise Unavailable(f"vendor {PARENT_VENDOR} is the parent's own")
    if not shutil.which(provider["bin"]):
        raise Unavailable(f"{provider['bin']} not on PATH")
    detect = provider.get("detect")
    if detect and subprocess.run(detect, capture_output=True, timeout=30).returncode:
        raise Unavailable(f"`{' '.join(detect)}` failed; not logged in")


def argv(provider, mode, values):
    parts = list(provider["review"]) if mode == "review" else provider["base"] + provider[mode]
    if provider.get("model"):
        parts += provider["model_args"]
    if provider.get("effort") and "effort_args" in provider:
        parts += provider["effort_args"]
    if mode != "review":
        parts += provider["prompt_args"]
    return [PLACEHOLDER.sub(lambda m: values[m[1]], part) for part in parts]


def failure(run):
    for text in (run.stderr, run.stdout):
        lines = [line for line in text.splitlines() if line.strip()]
        if lines:
            return lines[-1].strip()[:300]
    return "no output"


def attempt(provider, mode, cwd, prompt, out, timeout, base_ref):
    values = {
        "prompt": prompt,
        "base_ref": base_ref,
        "out": str(out),
        "model": provider.get("model", ""),
        "effort": provider.get("effort", ""),
    }
    try:
        run = subprocess.run(
            argv(provider, mode, values),
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise Unavailable(f"timed out after {int(timeout)}s") from None
    if run.returncode:
        raise Unavailable(f"exit {run.returncode}: {failure(run)}")

    if not out.is_file() or not out.read_text().strip():
        raise Unavailable("finished without a final message")
    match = re.search(provider["model_pattern"], run.stderr)
    return match[1] if match else provider.get("model") or "default"


def cmd_list(_args):
    order, providers = load()
    for name in order:
        provider = providers[name]
        try:
            check(provider)
            status = "ready" if provider.get("detect") else "installed; login not checked"
        except Unavailable as why:
            status = f"unavailable: {why}"
        model = provider.get("model") or "cli default"
        print(f"{name}\tvendor={provider['vendor']}\tmodel={model}\t{status}")
    for name in sorted(set(providers) - set(order)):
        print(f"{name}\tvendor={providers[name]['vendor']}\tnot in order")


def cmd_run(args):
    order, providers = load()
    if args.provider:
        if args.provider not in providers:
            sys.exit(f"peer: unknown provider {args.provider!r}")
        order = [args.provider]
    cwd = Path(args.cwd).resolve()
    if args.worktree:
        cwd = make_worktree(cwd, Path(args.worktree).resolve())
        log(f"worktree {cwd}")
    if args.mode == "write" and not is_linked_worktree(cwd):
        sys.exit(f"peer: write mode needs its own worktree; {cwd} is not one. Pass --worktree.")
    if args.base:
        try:
            git(cwd, "merge-base", "HEAD", args.base, text=True)
        except subprocess.CalledProcessError as e:
            sys.exit(f"peer: --base {args.base!r} has no merge base with HEAD: {e.stderr.strip()}")
    prompt = Path(args.prompt_file).read_text() if args.prompt_file else ""
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + args.timeout

    for name in order:
        provider = providers[name]
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            log(f"skip {name}: --timeout {args.timeout}s used up")
            continue
        before = git_state(cwd) if args.mode == "write" else None
        out.unlink(missing_ok=True)
        try:
            if args.mode == "review" and "review" not in provider:
                raise Unavailable("no review command")
            check(provider)
            model = attempt(provider, args.mode, cwd, prompt, out, remaining, args.base)
        except Unavailable as why:
            log(f"skip {name}: {why}")
            if before is not None and git_state(cwd) != before:
                log(f"{name} failed after editing {cwd}; not running another peer on its edits")
                return DIRTY_FAILURE
            continue
        print(f"peer provider={name} vendor={provider['vendor']} model={model} cwd={cwd} out={out}")
        return 0
    log("no peer could run")
    return NO_PEER


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="show each provider and whether it can run").set_defaults(
        func=cmd_list
    )
    run = sub.add_parser("run", help="run one brief on the first peer that can")
    run.add_argument("--mode", choices=["read-only", "write"], required=True)
    run.add_argument("--prompt-file", required=True)
    run.add_argument("--worktree", help="create this worktree from --cwd's repo and work there")
    run.set_defaults(base="")
    review = sub.add_parser("review", help="run the peer CLI's own read-only code review")
    review.add_argument("--base", required=True, help="branch the reviewed commits merge into")
    review.set_defaults(mode="review", prompt_file=None, worktree=None)
    for cmd in (run, review):
        cmd.add_argument("--out", required=True, help="file that receives the peer's final message")
        cmd.add_argument("--cwd", default=".", help="directory the peer works in")
        cmd.add_argument("--provider", help="run only this provider")
        cmd.add_argument("--timeout", type=int, default=1500, help="seconds across all attempts")
        cmd.set_defaults(func=cmd_run)
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
