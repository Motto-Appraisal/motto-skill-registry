#!/usr/bin/env python3
"""
Context Pack Manager — per-repo injectable context for session start.

Generates and manages structured context packs that capture architecture,
conventions, auth surfaces, known gotchas, and current state for a repo.
These packs inject at session start so droids start warm instead of re-exploring.

Usage:
  context-pack.py get <repo>           # Print the context pack for a repo
  context-pack.py list                 # List all available context packs
  context-pack.py create <repo>        # Create a new pack (interactive or from flags)
  context-pack.py update <repo> <section> <content>  # Update a section
  context-pack.py validate <repo>      # Validate pack structure
  context-pack.py path <repo>          # Print the file path for a pack

Pack structure (JSON):
  - repo: repo name/slug
  - repo_path: local checkout path
  - remote_url: git remote
  - architecture: high-level description of how the system works
  - key_files: {filename: description}
  - auth_surfaces: [{name, type, source, status}]
  - conventions: {branch_naming, test_cmd, lint_cmd, typecheck_cmd}
  - known_gotchas: [string]
  - current_state: {what_works, what_broken, what_dry_run}
  - how_to_run: string
  - dependencies: [string]
  - last_updated: ISO date
  - updated_by: session/droid identifier
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PACKS_DIR = Path(os.environ.get("CONTEXT_PACKS_DIR", str(Path.home() / ".factory" / "knowledge" / "context-packs")))

REQUIRED_SECTIONS = [
    "repo", "architecture", "key_files", "auth_surfaces",
    "conventions", "current_state", "how_to_run", "last_updated",
]


def pack_path(repo: str) -> Path:
    slug = repo.replace("/", "-").replace("\\", "-").replace(" ", "-").lower()
    return PACKS_DIR / f"{slug}.json"


def load_pack(repo: str) -> dict | None:
    p = pack_path(repo)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_pack(pack: dict) -> Path:
    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    p = pack_path(pack["repo"])
    p.write_text(json.dumps(pack, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def list_packs() -> list[dict]:
    if not PACKS_DIR.exists():
        return []
    packs = []
    for f in PACKS_DIR.glob("*.json"):
        try:
            pack = json.loads(f.read_text(encoding="utf-8"))
            packs.append({
                "repo": pack.get("repo", f.stem),
                "path": str(f),
                "last_updated": pack.get("last_updated", "unknown"),
                "architecture": pack.get("architecture", "")[:100],
            })
        except (json.JSONDecodeError, OSError):
            continue
    return packs


def validate_pack(pack: dict) -> list[str]:
    errors = []
    for section in REQUIRED_SECTIONS:
        if section not in pack:
            errors.append(f"Missing required section: {section}")
    return errors


def create_pack(
    repo: str,
    repo_path: str = "",
    remote_url: str = "",
    architecture: str = "",
    key_files: dict | None = None,
    auth_surfaces: list | None = None,
    conventions: dict | None = None,
    known_gotchas: list | None = None,
    current_state: dict | None = None,
    how_to_run: str = "",
    dependencies: list | None = None,
) -> dict:
    return {
        "repo": repo,
        "repo_path": repo_path,
        "remote_url": remote_url,
        "architecture": architecture,
        "key_files": key_files or {},
        "auth_surfaces": auth_surfaces or [],
        "conventions": conventions or {},
        "known_gotchas": known_gotchas or [],
        "current_state": current_state or {},
        "how_to_run": how_to_run,
        "dependencies": dependencies or [],
        "last_updated": datetime.now().isoformat(),
        "updated_by": os.environ.get("DROID_SESSION_ID", "manual"),
    }


def print_pack(pack: dict, format: str = "markdown") -> None:
    if format == "json":
        print(json.dumps(pack, indent=2, ensure_ascii=False))
        return

    # Markdown format for human reading
    print(f"# Context Pack: {pack['repo']}")
    print()
    if pack.get("repo_path"):
        print(f"**Path:** `{pack['repo_path']}`")
    if pack.get("remote_url"):
        print(f"**Remote:** {pack['remote_url']}")
    print(f"**Last updated:** {pack.get('last_updated', 'unknown')}")
    print()

    print("## Architecture")
    print(pack.get("architecture", "N/A"))
    print()

    if pack.get("key_files"):
        print("## Key Files")
        for fname, desc in pack["key_files"].items():
            print(f"- `{fname}`: {desc}")
        print()

    if pack.get("auth_surfaces"):
        print("## Auth Surfaces")
        for surface in pack["auth_surfaces"]:
            status_icon = {"solved": "OK", "blocked": "BLOCKED", "partial": "PARTIAL", "unknown": "?"}.get(
                surface.get("status", "unknown"), "?"
            )
            print(f"- [{status_icon}] {surface['name']} ({surface.get('type', 'unknown')}): {surface.get('source', '')} -> {surface.get('status', 'unknown')}")
        print()

    if pack.get("conventions"):
        print("## Conventions")
        conv = pack["conventions"]
        if conv.get("branch_naming"):
            print(f"- Branch: {conv['branch_naming']}")
        if conv.get("test_cmd"):
            print(f"- Test: `{conv['test_cmd']}`")
        if conv.get("lint_cmd"):
            print(f"- Lint: `{conv['lint_cmd']}`")
        if conv.get("typecheck_cmd"):
            print(f"- Typecheck: `{conv['typecheck_cmd']}`")
        print()

    if pack.get("known_gotchas"):
        print("## Known Gotchas")
        for gotcha in pack["known_gotchas"]:
            print(f"- {gotcha}")
        print()

    if pack.get("current_state"):
        print("## Current State")
        state = pack["current_state"]
        if state.get("what_works"):
            print(f"**Working:** {state['what_works']}")
        if state.get("what_broken"):
            print(f"**Broken:** {state['what_broken']}")
        if state.get("what_dry_run"):
            print(f"**Dry-run:** {state['what_dry_run']}")
        print()

    if pack.get("how_to_run"):
        print("## How to Run")
        print(f"```\n{pack['how_to_run']}\n```")
        print()

    if pack.get("dependencies"):
        print("## Dependencies")
        for dep in pack["dependencies"]:
            print(f"- {dep}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Context pack manager for per-repo injectable context")
    sub = parser.add_subparsers(dest="command")

    sp_get = sub.add_parser("get", help="Print the context pack for a repo")
    sp_get.add_argument("repo", help="Repo name or slug")
    sp_get.add_argument("--format", choices=["markdown", "json"], default="markdown")

    sub.add_parser("list", help="List all available context packs")

    sp_create = sub.add_parser("create", help="Create a new pack from a JSON file")
    sp_create.add_argument("repo", help="Repo name")
    sp_create.add_argument("--from-json", help="Path to JSON file with pack data")

    sp_update = sub.add_parser("update", help="Update a section of a pack")
    sp_update.add_argument("repo", help="Repo name")
    sp_update.add_argument("section", help="Section to update")
    sp_update.add_argument("content", help="New content (JSON string for objects, plain text for strings)")

    sp_validate = sub.add_parser("validate", help="Validate pack structure")
    sp_validate.add_argument("repo", help="Repo name")

    sp_path = sub.add_parser("path", help="Print the file path for a pack")
    sp_path.add_argument("repo", help="Repo name")

    args = parser.parse_args()

    if args.command == "get":
        pack = load_pack(args.repo)
        if not pack:
            print(f"No context pack found for: {args.repo}")
            print(f"Expected at: {pack_path(args.repo)}")
            sys.exit(1)
        print_pack(pack, args.format)

    elif args.command == "list":
        packs = list_packs()
        if not packs:
            print("No context packs found.")
            print(f"Packs directory: {PACKS_DIR}")
            return
        print(f"Context packs ({len(packs)}):")
        for p in packs:
            print(f"  {p['repo']:30} updated: {p['last_updated'][:10]}  {p['architecture'][:60]}")

    elif args.command == "create":
        if args.from_json:
            with open(args.from_json, "r", encoding="utf-8") as f:
                pack = json.load(f)
            pack["repo"] = args.repo
            pack["last_updated"] = datetime.now().isoformat()
        else:
            print("Use --from-json to provide pack data as a JSON file.")
            sys.exit(1)
        errors = validate_pack(pack)
        if errors:
            print("Validation errors:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        path = save_pack(pack)
        print(f"Created context pack: {path}")

    elif args.command == "update":
        pack = load_pack(args.repo)
        if not pack:
            print(f"No context pack found for: {args.repo}")
            sys.exit(1)
        # Try to parse content as JSON for object sections
        try:
            pack[args.section] = json.loads(args.content)
        except json.JSONDecodeError:
            pack[args.section] = args.content
        pack["last_updated"] = datetime.now().isoformat()
        save_pack(pack)
        print(f"Updated '{args.section}' in pack for {args.repo}")

    elif args.command == "validate":
        pack = load_pack(args.repo)
        if not pack:
            print(f"No context pack found for: {args.repo}")
            sys.exit(1)
        errors = validate_pack(pack)
        if errors:
            print(f"Validation FAILED ({len(errors)} errors):")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("Validation passed. All required sections present.")

    elif args.command == "path":
        print(pack_path(args.repo))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
