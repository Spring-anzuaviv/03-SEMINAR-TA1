#!/usr/bin/env python3
"""Verify the shared AGENTS.md and sources; --codex also checks the real loader."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PDF_SHA256 = "bc8b34cc847343151a496c2a515a7178bf90a834d5bee909bddcf56179bd218e"
SPEC_SHA256 = "13d2d1412f08521327738c8871294a7e03e7212f93a0a609f073d1b19b0a2b46"
LEGACY_PATHS = (".agents", ".codex", ".claude", ".cursor", "CLAUDE.md",
                "scripts/sync_agent_config.py")
RULES = {"sources.md": "Nguồn yêu cầu", "common.md": "Quy tắc chung",
         "payment-scope.md": "Phạm vi Bảng thanh toán", "handoff.md": "Bàn giao và nhật ký",
         "ba.md": "Vai trò ba", "design.md": "Vai trò design", "reviewer.md": "Vai trò reviewer"}
SKILLS = ("naming-versioning", "sys-spec", "uml-diagrams", "sequence-diagram",
          "data-design", "traceability-matrix")

VERSIONS = ("v1", "v2")
OPS = "create|update|submit|approve|reject|adjust|cancel"
ANALYSIS_RE = r"(sys-us-0[1-5]|open-questions|requirements-checklist|requirements-analysis)-{v}\.md"
DESIGN_RE = (r"(01-requirements-summary|02-architecture-design|03-detailed-design|"
             r"04-api-contract|05-data-design|06-traceability-matrix|"
             r"07-design-decisions|08-handoff-to-developer)-{v}\.md")
DIAGRAM_RE = (r"(seq-us-0[1-5](-(" + OPS + r"))?|component|class|state-machine|erd|"
              r"use-case|activity-(" + OPS + r"))-{v}\.(puml|svg|png)")
REVIEW_RE = r"(ai-review|review-assessment|user-review)-(\d{2}|us-0[1-5])(-v[12])?\.md|evaluation-report\.md"
ALWAYS_OK = (".gitkeep", "README.md")
USE_CASE_FOLDERS = tuple(f"us-pay-{number:02}" for number in range(1, 6))


def naming_problems():
    """Return file names that break skills/naming-versioning (empty list = OK)."""
    problems = []

    def scan(folder, pattern, recurse_into=()):
        if not folder.is_dir():
            return
        for item in sorted(folder.iterdir()):
            rel = item.relative_to(ROOT).as_posix()
            if " " in item.name:
                problems.append(rel + " (khoảng trắng)")
            if item.is_dir():
                if item.name not in recurse_into:
                    problems.append(rel + "/ (thư mục ngoài quy ước)")
                continue
            if item.name in ALWAYS_OK:
                continue
            if not re.fullmatch(pattern, item.name):
                problems.append(rel)
            elif item.suffix == ".puml":
                match = re.search(r"^@startuml\s+(\S+)", item.read_text(encoding="utf-8-sig"),
                                  re.MULTILINE)
                if not match or match.group(1) != item.stem:
                    problems.append(rel + " (@startuml phải trùng tên file)")

    for parent, allowed in (("docs/analysis/payment-management", ()),
                            ("docs/design/payment-management", ("diagrams",))):
        base = ROOT / parent
        for item in sorted(base.iterdir()) if base.is_dir() else ():
            if item.is_dir() and item.name not in VERSIONS:
                problems.append(item.relative_to(ROOT).as_posix() + "/ (chỉ dùng v1, v2)")
        for v in VERSIONS:
            if parent.startswith("docs/analysis"):
                scan(base / v, ANALYSIS_RE.format(v=v))
            else:
                scan(base / v, DESIGN_RE.format(v=v), allowed + USE_CASE_FOLDERS)
                scan(base / v / "diagrams", DIAGRAM_RE.format(v=v))
                for folder in USE_CASE_FOLDERS:
                    number = folder[-2:]
                    pattern = (rf"(sys-us-{number}|open-questions)-{v}\.md|"
                               rf"seq-us-{number}(-({OPS}))?-{v}\.(puml|svg|png)")
                    scan(base / v / folder, pattern)
    scan(ROOT / "docs/review/payment-management", REVIEW_RE)
    return problems


def text_values(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "text" and isinstance(child, str):
                yield child
            else:
                yield from text_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from text_values(child)


def verify(codex=False):
    failures = []

    def check(condition, label):
        print(f"{'PASS' if condition else 'FAIL'}: {label}")
        if not condition:
            failures.append(label)

    guidance = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for name, heading in RULES.items():
        path = ROOT / "rules" / name
        check(path.is_file() and path.read_text(encoding="utf-8").startswith(
            f"# Rule – {heading}\n"), f"rule file: rules/{name} ({heading})")
        check(f"](rules/{name})" in guidance, f"AGENTS.md links rule: rules/{name}")
    check(not re.search(r"(?m)^## (Quy tắc chung|Vai trò (ba|design|reviewer))$", guidance),
          "rules live only in rules/ (not duplicated in AGENTS.md)")
    for relative in LEGACY_PATHS:
        check(not (ROOT / relative).exists(),
              "separate configuration removed: " + relative)
        check(relative not in guidance, "no obsolete instruction reference: " + relative)

    for relative in ("README.md", "docs/workflow/README.md", "docs/workflow/prompt-log.md",
                     "docs/requirements/payment-management/sources.md",
                     "docs/analysis/payment-management/v1",
                     "docs/analysis/payment-management/v2",
                     "docs/design/payment-management/v1/diagrams",
                     "docs/design/payment-management/v2/diagrams",
                     "docs/review/payment-management"):
        check((ROOT / relative).exists(), "workspace path: " + relative)
    skill_docs = ["skills/README.md", "skills/_shared/payment-context.md"]
    for name in SKILLS:
        relative = f"skills/{name}/SKILL.md"
        path = ROOT / relative
        check(path.is_file() and path.read_text(encoding="utf-8").startswith(
            f"---\nname: {name}\n"), "skill with front matter: " + relative)
        skill_docs.append(relative)
    for relative, digest in (
        ("docs/requirements/payment-management/assignment-ta-1-2.pdf", PDF_SHA256),
        ("docs/requirements/payment-management/spec.md", SPEC_SHA256),
    ):
        path = ROOT / relative
        data = path.read_bytes() if path.is_file() else b""
        if relative.endswith(".md"):  # Git on Windows may check out CRLF
            data = data.replace(b"\r\n", b"\n")
        check(path.is_file() and hashlib.sha256(data).hexdigest() == digest,
              "source preserved (SHA-256): " + relative)

    setup_docs = ["AGENTS.md", "README.md", "rules/README.md",
                  *(f"rules/{name}" for name in RULES), "docs/workflow/README.md",
                  "docs/workflow/prompt-log.md",
                  "docs/requirements/payment-management/spec.md",
                  "docs/requirements/payment-management/sources.md",
                  "docs/analysis/payment-management/README.md",
                  "docs/design/payment-management/README.md",
                  "docs/review/payment-management/README.md"] + skill_docs
    for relative in setup_docs:
        path = ROOT / relative
        if not path.is_file():
            check(False, "local links: " + relative + " (file missing)")
            continue
        content = path.read_text(encoding="utf-8")
        missing = []
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if not (path.parent / target).exists():
                missing.append(target)
        check(not missing, "local links: " + relative +
              (f" missing {missing}" if missing else ""))

    problems = naming_problems()
    check(not problems, "naming-versioning: file names in v1/v2 and review" +
          (f" invalid {problems}" if problems else ""))

    if codex:
        executable = shutil.which("codex")
        check(bool(executable), "Codex executable available")
        if executable:
            version = subprocess.run([executable, "--version"], capture_output=True,
                                     text=True, timeout=15)
            print("INFO: " + version.stdout.strip())
            result = subprocess.run(
                [executable, "debug", "prompt-input", "Kiểm tra nạp file chung, không làm tác vụ khác."],
                cwd=ROOT, capture_output=True, text=True, timeout=60)
            check(result.returncode == 0, "Codex real prompt loader ran")
            if result.returncode:
                print("INFO: Inspect local Codex availability and terminal permissions; "
                      "raw prompts/configuration are not printed.")
            else:
                items = json.loads(result.stdout)
                project_texts = [
                    text for item in items
                    if item.get("type") == "message" and item.get("role") == "user"
                    for text in text_values(item.get("content", []))
                ]
                check(any(guidance.rstrip() in text for text in project_texts),
                      "Codex loaded complete shared AGENTS.md")
                print("INFO: Shared rules and all three role definitions checked together; "
                      "no model call or business-agent execution was performed.")
    print(f"RESULT: {'FAIL' if failures else 'PASS'} ({len(failures)} failed checks)")
    return bool(failures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", action="store_true",
                        help="Inspect local Codex prompt loader without a model call")
    args = parser.parse_args()
    try:
        sys.exit(verify(args.codex))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
