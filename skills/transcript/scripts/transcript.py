#!/usr/bin/env python3
"""Find and read the active Claude Code run's transcript.

transcript.py path
    Print the absolute path of this run's transcript. Exit 1 if it cannot be found exactly.
transcript.py subagents FILE
    Print the transcripts of subagents that FILE's run spawned.
transcript.py digest FILE [--from N] [--width W]
    Print one numbered line per message or tool call. Cite the number, open the raw
    record with: sed -n '<N>p' FILE
"""

import argparse
import json
import os
import sys
from pathlib import Path

VAR = "CLAUDE_CODE_SESSION_ID"


def find():
    run_id = os.environ.get(VAR)
    if not run_id:
        sys.exit(f"transcript: ${VAR} is not set; is this a Claude Code session?")
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
    matches = sorted(home.glob(f"projects/*/{run_id}.jsonl"))
    if len(matches) != 1:
        sys.exit(f"transcript: expected one transcript for {VAR}={run_id}, found {len(matches)}")
    return matches[0]


def subagents(path):
    path = Path(path)
    return sorted((path.parent / path.stem / "subagents").glob("*.jsonl"))


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(text_of(part) for part in content)
    if isinstance(content, dict):
        for key in ("text", "content", "output"):
            if key in content:
                return text_of(content[key])
    return ""


def entries(record):
    kind = record.get("type")
    if kind not in ("user", "assistant"):
        return
    prefix = "sidechain " if record.get("isSidechain") else ""
    content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        yield prefix + kind, content
        return
    for part in content or []:
        part_type = part.get("type")
        if part_type == "text":
            yield prefix + kind, part.get("text", "")
        elif part_type == "tool_use":
            yield prefix + "tool_use", f"{part.get('name')} {json.dumps(part.get('input'))}"
        elif part_type == "tool_result":
            yield prefix + "tool_result", text_of(part.get("content"))


def digest(path, start, width):
    with Path(path).open() as lines:
        for number, line in enumerate(lines, 1):
            if number < start:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            for role, text in entries(record):
                flat = " ".join(text.split())
                if flat:
                    print(f"L{number} {role}: {flat[:width]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("path")
    sub.add_parser("subagents").add_argument("file")
    digest_cmd = sub.add_parser("digest")
    digest_cmd.add_argument("file")
    digest_cmd.add_argument("--from", dest="start", type=int, default=1)
    digest_cmd.add_argument("--width", type=int, default=300)
    args = parser.parse_args()
    if args.command == "path":
        print(find())
    elif args.command == "subagents":
        for child in subagents(args.file):
            print(child)
    else:
        digest(args.file, args.start, args.width)


if __name__ == "__main__":
    main()
