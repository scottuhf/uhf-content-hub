#!/usr/bin/env python3
"""
Context Keeper — Claude Session Compression & Rehydration Tool
Inspired by DeepSeek's OCR compression approach for managing context density.

Usage:
  python context_keeper.py compress    # Compress current session context
  python context_keeper.py rehydrate   # Generate rehydration prompt for new session
  python context_keeper.py list        # List all saved snapshots
  python context_keeper.py view <id>   # View a specific snapshot
  python context_keeper.py diff <id1> <id2>  # Compare two snapshots
  python context_keeper.py export <id> # Export snapshot as markdown
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
import hashlib
import textwrap


# ── Config ─────────────────────────────────────────────────────────────────────

STORE_DIR = Path.home() / ".context-keeper"
SNAPSHOTS_DIR = STORE_DIR / "snapshots"
PROJECTS_FILE = STORE_DIR / "projects.json"

CONTEXTS = ["uhf", "dev", "research", "writing", "general"]  # project types

COLORS = {
    "header":   "\033[1;36m",  # bold cyan
    "success":  "\033[1;32m",  # bold green
    "warning":  "\033[1;33m",  # bold yellow
    "error":    "\033[1;31m",  # bold red
    "muted":    "\033[0;90m",  # dark gray
    "bold":     "\033[1m",
    "reset":    "\033[0m",
}

def c(color, text):
    """Apply terminal color."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


# ── Storage ─────────────────────────────────────────────────────────────────────

def ensure_dirs():
    STORE_DIR.mkdir(exist_ok=True)
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    if not PROJECTS_FILE.exists():
        PROJECTS_FILE.write_text(json.dumps({"projects": {}}, indent=2))

def load_projects():
    return json.loads(PROJECTS_FILE.read_text())

def save_projects(data):
    PROJECTS_FILE.write_text(json.dumps(data, indent=2))

def snapshot_path(snapshot_id):
    return SNAPSHOTS_DIR / f"{snapshot_id}.json"

def save_snapshot(snapshot):
    path = snapshot_path(snapshot["id"])
    path.write_text(json.dumps(snapshot, indent=2))
    return path

def load_snapshot(snapshot_id):
    path = snapshot_path(snapshot_id)
    if not path.exists():
        print(c("error", f"  Snapshot '{snapshot_id}' not found."))
        sys.exit(1)
    return json.loads(path.read_text())

def all_snapshots():
    snapshots = []
    for f in sorted(SNAPSHOTS_DIR.glob("*.json"), reverse=True):
        try:
            snapshots.append(json.loads(f.read_text()))
        except Exception:
            pass
    return snapshots

def generate_id(project, ts):
    raw = f"{project}-{ts}"
    return hashlib.md5(raw.encode()).hexdigest()[:8]


# ── Compression ─────────────────────────────────────────────────────────────────

COMPRESS_QUESTIONS = [
    ("project",         "Project name (e.g. uhf-content-hub, my-api, podcast-scripts)"),
    ("context_type",    f"Context type [{'/'.join(CONTEXTS)}]"),
    ("goal",            "What is the overarching goal of this project/session?"),
    ("current_status",  "What's the current status? (what's done, what's in progress)"),
    ("blockers",        "Any blockers or open questions? (or 'none')"),
    ("key_decisions",   "Key decisions made so far (comma-separated, or 'none')"),
    ("next_steps",      "What are the immediate next steps? (comma-separated)"),
    ("file_paths",      "Key file paths or URLs to remember (comma-separated, or 'none')"),
    ("tech_stack",      "Tech stack / tools in use (comma-separated, or 'none')"),
    ("notes",           "Any extra context Claude should know to resume effectively? (or 'none')"),
]

def prompt_input(label, hint=None):
    print(c("muted", f"  {label}"))
    if hint:
        print(c("muted", f"  → {hint}"))
    val = input("  > ").strip()
    print()
    return val if val.lower() != "none" else ""

def compress():
    ensure_dirs()
    print()
    print(c("header", "  ╔══════════════════════════════════════════╗"))
    print(c("header", "  ║        Context Keeper — Compress         ║"))
    print(c("header", "  ╚══════════════════════════════════════════╝"))
    print()
    print(c("muted", "  Capture the key context from your current session."))
    print(c("muted", "  Answer each prompt — be concise but specific.\n"))

    data = {}
    for key, label in COMPRESS_QUESTIONS:
        data[key] = prompt_input(label)

    # Parse list fields
    for field in ["key_decisions", "next_steps", "file_paths", "tech_stack"]:
        if data[field]:
            data[field] = [x.strip() for x in data[field].split(",") if x.strip()]
        else:
            data[field] = []

    ts = datetime.now().isoformat()
    snapshot_id = generate_id(data["project"], ts)

    snapshot = {
        "id": snapshot_id,
        "created_at": ts,
        "version": 1,
        **data
    }

    # Version tracking — find prior snapshots for same project and bump version
    existing = [s for s in all_snapshots() if s.get("project") == data["project"]]
    if existing:
        latest = max(existing, key=lambda s: s.get("version", 1))
        snapshot["version"] = latest["version"] + 1
        snapshot["previous_id"] = latest["id"]

    save_snapshot(snapshot)

    # Update project index
    projects = load_projects()
    projects["projects"][data["project"]] = {
        "latest_snapshot": snapshot_id,
        "last_updated": ts,
        "version": snapshot["version"],
    }
    save_projects(projects)

    print(c("success", f"  ✓ Snapshot saved [{snapshot_id}]"))
    print(c("muted",   f"    Project : {data['project']}"))
    print(c("muted",   f"    Version : v{snapshot['version']}"))
    print(c("muted",   f"    Stored  : {snapshot_path(snapshot_id)}"))
    print()
    print(c("bold", "  Run `python context_keeper.py rehydrate` to generate your resume prompt.\n"))

    return snapshot_id


# ── Rehydration ─────────────────────────────────────────────────────────────────

def build_rehydration_prompt(snapshot):
    """Build a dense, Claude-optimized rehydration prompt."""
    s = snapshot
    ts = datetime.fromisoformat(s["created_at"]).strftime("%b %d, %Y at %H:%M")

    lines = [
        "# SESSION REHYDRATION CONTEXT",
        f"_Snapshot: {s['id']} | {ts} | v{s['version']}_",
        "",
        "---",
        "",
        f"## Project: {s['project']}",
        f"**Type:** {s.get('context_type', 'general')}",
        "",
        f"## Goal",
        s["goal"],
        "",
        f"## Current Status",
        s["current_status"],
    ]

    if s.get("key_decisions"):
        lines += ["", "## Key Decisions Made"]
        for d in s["key_decisions"]:
            lines.append(f"- {d}")

    if s.get("next_steps"):
        lines += ["", "## Immediate Next Steps"]
        for i, step in enumerate(s["next_steps"], 1):
            lines.append(f"{i}. {step}")

    if s.get("blockers"):
        lines += ["", f"## Open Blockers / Questions", s["blockers"]]

    if s.get("tech_stack"):
        lines += ["", f"## Tech Stack", ", ".join(s["tech_stack"])]

    if s.get("file_paths"):
        lines += ["", "## Key File Paths / URLs"]
        for fp in s["file_paths"]:
            lines.append(f"- `{fp}`")

    if s.get("notes"):
        lines += ["", "## Additional Context", s["notes"]]

    lines += [
        "",
        "---",
        "",
        "_You are resuming this project. Acknowledge the context above, ask for any "
        "clarification if needed, and continue from where we left off._",
    ]

    return "\n".join(lines)


def rehydrate(project=None):
    ensure_dirs()
    snapshots = all_snapshots()
    if not snapshots:
        print(c("error", "\n  No snapshots found. Run `compress` first.\n"))
        sys.exit(1)

    if project:
        candidates = [s for s in snapshots if s.get("project") == project]
        if not candidates:
            print(c("error", f"\n  No snapshots for project '{project}'.\n"))
            sys.exit(1)
        snapshot = max(candidates, key=lambda s: s.get("version", 1))
    else:
        # Let user pick from recent snapshots
        print()
        print(c("header", "  ╔══════════════════════════════════════════╗"))
        print(c("header", "  ║       Context Keeper — Rehydrate         ║"))
        print(c("header", "  ╚══════════════════════════════════════════╝"))
        print()

        recent = snapshots[:10]
        for i, s in enumerate(recent):
            ts = datetime.fromisoformat(s["created_at"]).strftime("%b %d %H:%M")
            print(c("bold", f"  [{i+1}] ") +
                  c("muted", f"{s['project']:<24} v{s['version']:<4} {ts}  ") +
                  c("muted", f"[{s['id']}]"))

        print()
        choice = input(c("muted", "  Select snapshot number (or press Enter for latest): ")).strip()
        if not choice:
            snapshot = recent[0]
        else:
            try:
                snapshot = recent[int(choice) - 1]
            except (ValueError, IndexError):
                print(c("error", "  Invalid selection.\n"))
                sys.exit(1)

    prompt = build_rehydration_prompt(snapshot)

    print()
    print(c("header", "  ╔══════════════════════════════════════════════════════════════╗"))
    print(c("header", "  ║  REHYDRATION PROMPT — paste this at the start of a new chat  ║"))
    print(c("header", "  ╚══════════════════════════════════════════════════════════════╝"))
    print()
    print(prompt)
    print()

    # Also write to clipboard file for easy access
    out_file = STORE_DIR / f"rehydrate_{snapshot['id']}.md"
    out_file.write_text(prompt)
    print(c("success", f"  ✓ Also saved to: {out_file}\n"))


# ── List ─────────────────────────────────────────────────────────────────────────

def list_snapshots(project_filter=None):
    ensure_dirs()
    snapshots = all_snapshots()
    if project_filter:
        snapshots = [s for s in snapshots if s.get("project") == project_filter]

    if not snapshots:
        print(c("muted", "\n  No snapshots found.\n"))
        return

    print()
    print(c("header", "  Saved Snapshots"))
    print(c("muted", "  " + "─" * 70))

    current_project = None
    for s in snapshots:
        if s.get("project") != current_project:
            current_project = s.get("project")
            print()
            print(c("bold", f"  {current_project}"))

        ts = datetime.fromisoformat(s["created_at"]).strftime("%b %d, %Y  %H:%M")
        status_preview = s.get("current_status", "")[:45]
        if len(s.get("current_status", "")) > 45:
            status_preview += "..."

        print(f"  {c('muted', ts)}  v{s['version']:<3}  [{s['id']}]")
        print(c("muted", f"    {status_preview}"))

    print()


# ── View ─────────────────────────────────────────────────────────────────────────

def view_snapshot(snapshot_id):
    ensure_dirs()
    snapshot = load_snapshot(snapshot_id)
    s = snapshot
    ts = datetime.fromisoformat(s["created_at"]).strftime("%B %d, %Y at %H:%M")

    print()
    print(c("header", f"  Snapshot {s['id']}  —  {s['project']}  v{s['version']}"))
    print(c("muted", f"  Captured: {ts}"))
    print(c("muted", "  " + "─" * 60))
    print()

    def show(label, value):
        if not value:
            return
        print(c("bold", f"  {label}"))
        if isinstance(value, list):
            for item in value:
                print(c("muted", f"    • {item}"))
        else:
            for line in textwrap.wrap(value, 70):
                print(c("muted", f"    {line}"))
        print()

    show("Goal", s.get("goal"))
    show("Status", s.get("current_status"))
    show("Blockers", s.get("blockers"))
    show("Key Decisions", s.get("key_decisions"))
    show("Next Steps", s.get("next_steps"))
    show("Tech Stack", s.get("tech_stack"))
    show("File Paths", s.get("file_paths"))
    show("Notes", s.get("notes"))


# ── Diff ─────────────────────────────────────────────────────────────────────────

def diff_snapshots(id1, id2):
    ensure_dirs()
    s1 = load_snapshot(id1)
    s2 = load_snapshot(id2)

    text_fields = ["goal", "current_status", "blockers", "notes"]
    list_fields = ["key_decisions", "next_steps", "file_paths", "tech_stack"]

    print()
    print(c("header", f"  Diff: {id1} (v{s1['version']}) → {id2} (v{s2['version']})"))
    print(c("muted", "  " + "─" * 60))
    print()

    for field in text_fields:
        v1, v2 = s1.get(field, ""), s2.get(field, "")
        if v1 != v2:
            print(c("bold", f"  {field.replace('_', ' ').title()}"))
            print(c("error",   f"  - {v1 or '(empty)'}"))
            print(c("success", f"  + {v2 or '(empty)'}"))
            print()

    for field in list_fields:
        l1 = set(s1.get(field, []))
        l2 = set(s2.get(field, []))
        removed = l1 - l2
        added   = l2 - l1
        if removed or added:
            print(c("bold", f"  {field.replace('_', ' ').title()}"))
            for item in sorted(removed):
                print(c("error",   f"  - {item}"))
            for item in sorted(added):
                print(c("success", f"  + {item}"))
            print()

    if not any(
        s1.get(f) != s2.get(f)
        for f in text_fields + list_fields
    ):
        print(c("muted", "  No differences found.\n"))


# ── Export ─────────────────────────────────────────────────────────────────────

def export_snapshot(snapshot_id):
    ensure_dirs()
    snapshot = load_snapshot(snapshot_id)
    prompt = build_rehydration_prompt(snapshot)
    out_file = Path.cwd() / f"context_{snapshot_id}.md"
    out_file.write_text(prompt)
    print(c("success", f"\n  ✓ Exported to: {out_file}\n"))


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Context Keeper — Claude session compression & rehydration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
          Commands:
            compress              Compress current session into a snapshot
            rehydrate [project]   Generate rehydration prompt (optionally for a project)
            list [project]        List all saved snapshots
            view <id>             View a specific snapshot
            diff <id1> <id2>      Compare two snapshots
            export <id>           Export snapshot as a markdown file
        """)
    )
    parser.add_argument("command", choices=["compress", "rehydrate", "list", "view", "diff", "export"])
    parser.add_argument("args", nargs="*", help="Optional arguments")
    args = parser.parse_args()

    if args.command == "compress":
        compress()
    elif args.command == "rehydrate":
        rehydrate(args.args[0] if args.args else None)
    elif args.command == "list":
        list_snapshots(args.args[0] if args.args else None)
    elif args.command == "view":
        if not args.args:
            print(c("error", "\n  Usage: view <snapshot-id>\n"))
            sys.exit(1)
        view_snapshot(args.args[0])
    elif args.command == "diff":
        if len(args.args) < 2:
            print(c("error", "\n  Usage: diff <id1> <id2>\n"))
            sys.exit(1)
        diff_snapshots(args.args[0], args.args[1])
    elif args.command == "export":
        if not args.args:
            print(c("error", "\n  Usage: export <snapshot-id>\n"))
            sys.exit(1)
        export_snapshot(args.args[0])


if __name__ == "__main__":
    main()
