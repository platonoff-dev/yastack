#!/usr/bin/env python3
"""Validate yastack invariants. See AGENTS.md#invariants."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ENTRY = "yastack"
PRINCIPLE = "principle-"
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
ITEM = re.compile(r"^- \*\*[^*]+\*\* \(`([a-z0-9-]+)`\)\.", re.M)

errors = []


def frontmatter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def section(text, heading):
    match = re.search(rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        errors.append(f"skills/{ENTRY}/SKILL.md: missing '## {heading}' section")
        return set()
    return set(ITEM.findall(match.group(1)))


def rel(path):
    return path.relative_to(ROOT)


skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())

for skill in skill_dirs:
    md = skill / "SKILL.md"
    if not md.is_file():
        errors.append(f"{rel(skill)}: no SKILL.md")
        continue
    fm = frontmatter(md)
    if fm is None:
        errors.append(f"{rel(md)}: missing or malformed frontmatter")
        continue
    if fm.get("name") != skill.name:
        errors.append(f"{rel(md)}: name is {fm.get('name')!r}, expected {skill.name!r}")
    if not fm.get("description"):
        errors.append(f"{rel(md)}: empty description")
    if fm.get("disable-model-invocation") != "true":
        errors.append(f"{rel(md)}: needs 'disable-model-invocation: true'")

    yaml = skill / "agents" / "openai.yaml"
    if not yaml.is_file():
        errors.append(f"{rel(skill)}: no agents/openai.yaml")
    elif not re.search(r"^\s+allow_implicit_invocation:\s*false\s*$", yaml.read_text(), re.M):
        errors.append(f"{rel(yaml)}: needs 'policy.allow_implicit_invocation: false'")

    for doc in skill.rglob("*.md"):
        for target in LINK.findall(doc.read_text()):
            if "://" in target or target.startswith("mailto:"):
                continue
            if not (doc.parent / target).exists():
                errors.append(f"{rel(doc)}: broken link {target}")

entry_md = SKILLS / ENTRY / "SKILL.md"
if entry_md.is_file():
    text = entry_md.read_text()
    names = {p.name for p in skill_dirs} - {ENTRY}
    playbook_dir = SKILLS / ENTRY / "playbooks"
    playbooks = {p.stem for p in playbook_dir.glob("*.md")} if playbook_dir.is_dir() else set()
    principles = {n for n in names if n.startswith(PRINCIPLE)}

    for heading, present, kind in (
        ("Playbooks", playbooks, "playbook"),
        ("Principles", principles, "principle"),
    ):
        listed = section(text, heading)
        for name in sorted(present - listed):
            errors.append(f"{kind} {name}: not under '## {heading}' in the entry point")
        for name in sorted(listed - present):
            errors.append(f"skills/{ENTRY}/SKILL.md: '## {heading}' lists missing {kind} {name!r}")

    seen = set()
    todo = [entry_md]
    todo += [playbook_dir / f"{n}.md" for n in playbooks]
    todo += [SKILLS / n / "SKILL.md" for n in principles]
    while todo:
        doc = todo.pop().resolve()
        if doc in seen or not doc.is_file():
            continue
        seen.add(doc)
        for target in LINK.findall(doc.read_text()):
            if "://" not in target and target.endswith(".md"):
                todo.append(doc.parent / target)
    reached = {d.relative_to(SKILLS).parts[0] for d in seen if d.is_relative_to(SKILLS)}
    for name in sorted(names - principles - reached):
        errors.append(f"skills/{name}: unreachable, nothing links to it from the entry point")
else:
    errors.append(f"skills/{ENTRY}/SKILL.md: entry point missing")

for error in errors:
    print(error)
if errors:
    sys.exit(1)
print(f"ok: {len(skill_dirs)} skill(s)")
