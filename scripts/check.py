#!/usr/bin/env python3
"""Validate yastack invariants. See CLAUDE.md#invariants."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
ENTRY = "yastack"
PRINCIPLES = "principles"
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
ITEM = re.compile(r"^- \*\*[^*]+\*\* \(`([a-z0-9-]+)`\)\.", re.M)
PRINCIPLE_ITEM = re.compile(r"^- \[[^\]]+\]\(([a-z0-9-]+)\.md\)\.", re.M)
OTHER_HARNESS = re.compile(r"\bcodex\b|spawn_agent|allow_implicit_invocation", re.I)
SKILL_NAME = re.compile(r"`([a-z0-9-]+)`")
UP_PATH = re.compile(r"(?<![\w./])(?:\.\./)+[^\s)`'\"]+")
PRINCIPLE_REF = re.compile(r"((?:`[a-z0-9-]+`(?:,? and |,? or |, ))*`[a-z0-9-]+`) principles?\b")
TODOLIST = re.compile(r"\btodo[ -]?lists?\b", re.I)

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
    # Only the entry point is user-only. Every other skill must stay loadable with the Skill tool.
    user_only = skill.name == ENTRY
    if (fm.get("disable-model-invocation") == "true") != user_only:
        want = "'disable-model-invocation: true'" if user_only else "no 'disable-model-invocation'"
        errors.append(f"{rel(md)}: needs {want}")

# A path resolves only against the loaded skill's base directory, so links and paths stay inside
# one skill. Reach a skill with Skill, a principle through the principles skill, a playbook only
# from yastack.
for doc in sorted([*SKILLS.rglob("*.md"), *(ROOT / ".claude" / "skills").rglob("*.md")]):
    text = doc.read_text()
    home = next(p for p in doc.parents if (p / "SKILL.md").is_file()).resolve()
    targets = [t for t in LINK.findall(text) if "://" not in t and not t.startswith("mailto:")]
    for target in dict.fromkeys([*targets, *UP_PATH.findall(text)]):
        dest = (doc.parent / target.split("#")[0]).resolve()
        if not dest.is_relative_to(home):
            fix = "name the skill"
            if PRINCIPLES in dest.parts:
                fix = "name the principle"
            elif "playbooks" in dest.parts:
                fix = "put the rule in this skill"
            errors.append(f"{rel(doc)}: {target} leaves {home.name}/; {fix} instead")
        elif target in targets and not dest.exists():
            errors.append(f"{rel(doc)}: broken link {target}")
    if doc.is_relative_to(SKILLS) and home.name != ENTRY and "playbooks/" in text:
        errors.append(f"{rel(doc)}: refers to a playbook; only {ENTRY} can locate one")

# yastack is tuned to Claude Code only. Keep other harnesses out of every skill.
for path in sorted([*SKILLS.rglob("*"), *(ROOT / ".claude" / "skills").rglob("*")]):
    if not path.is_file():
        continue
    if path.name == "openai.yaml":
        errors.append(f"{rel(path)}: Codex metadata; yastack targets Claude Code only")
    elif OTHER_HARNESS.search(path.read_text(errors="ignore")):
        errors.append(f"{rel(path)}: mentions Codex; yastack targets Claude Code only")

# Outside the index, a principle is "the `<name>` principle". Its skill loads the principles skill,
# because a name alone gets cited, not read.
principle_names = {p.stem for p in (SKILLS / PRINCIPLES).glob("*.md")} - {"SKILL"}
for skill in skill_dirs:
    if skill.name == PRINCIPLES:
        continue
    named = False
    for doc in sorted(skill.rglob("*.md")):
        text = doc.read_text()
        refs = {n for group in PRINCIPLE_REF.findall(text) for n in SKILL_NAME.findall(group)}
        for name in sorted(refs - principle_names - {p.name for p in skill_dirs}):
            errors.append(f"{rel(doc)}: names missing principle {name!r}")
        for name in sorted(set(SKILL_NAME.findall(text)) & principle_names - refs):
            errors.append(f"{rel(doc)}: write `{name}` as 'the `{name}` principle'")
        named |= bool(refs & principle_names)
    text = "".join(d.read_text() for d in skill.rglob("*.md"))
    if named and f"`{PRINCIPLES}` skill" not in text:
        errors.append(f"skills/{skill.name}: names a principle but never the `principles` skill")

# "Open a todolist" names no Claude Code tool. Use the router's checklist and TaskCreate rule.
for path in sorted(SKILLS.rglob("*.md")):
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if TODOLIST.search(line):
            errors.append(f"{rel(path)}:{n}: says 'todolist'; use the router's checklist rule")

entry_md = SKILLS / ENTRY / "SKILL.md"
if entry_md.is_file():
    text = entry_md.read_text()
    names = {p.name for p in skill_dirs} - {ENTRY}
    playbook_dir = SKILLS / ENTRY / "playbooks"
    playbooks = {p.stem for p in playbook_dir.glob("*.md")} if playbook_dir.is_dir() else set()

    listed = section(text, "Playbooks")
    for name in sorted(playbooks - listed):
        errors.append(f"playbook {name}: not under '## Playbooks' in the entry point")
    for name in sorted(listed - playbooks):
        errors.append(f"skills/{ENTRY}/SKILL.md: '## Playbooks' lists missing playbook {name!r}")

    index = SKILLS / PRINCIPLES / "SKILL.md"
    if index.is_file():
        present = {p.stem for p in index.parent.glob("*.md")} - {"SKILL"}
        listed = set(PRINCIPLE_ITEM.findall(index.read_text()))
        for name in sorted(present - listed):
            errors.append(
                f"skills/{PRINCIPLES}/{name}.md: not listed as '- [Title]({name}.md).' in the index"
            )
        for name in sorted(listed - present):
            errors.append(f"skills/{PRINCIPLES}/SKILL.md: lists missing principle {name!r}")

    seen = set()
    todo = [entry_md]
    todo += [playbook_dir / f"{n}.md" for n in playbooks]
    while todo:
        doc = todo.pop().resolve()
        if doc in seen or not doc.is_file():
            continue
        seen.add(doc)
        text = doc.read_text()
        for target in LINK.findall(text):
            if "://" not in target and target.endswith(".md"):
                todo.append(doc.parent / target)
        for name in SKILL_NAME.findall(text):
            if name in names | {PRINCIPLES}:
                todo.append(SKILLS / name / "SKILL.md")
    reached = {d.relative_to(SKILLS).parts[0] for d in seen if d.is_relative_to(SKILLS)}
    for name in sorted(names - reached):
        errors.append(f"skills/{name}: unreachable, nothing names it from the entry point")
else:
    errors.append(f"skills/{ENTRY}/SKILL.md: entry point missing")

for error in errors:
    print(error)
if errors:
    sys.exit(1)
print(f"ok: {len(skill_dirs)} skill(s)")
