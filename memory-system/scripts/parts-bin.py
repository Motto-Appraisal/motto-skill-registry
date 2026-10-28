#!/usr/bin/env python3
"""
Parts-Bin Catalog — memoized recycler decisions.

Stores "reuse X vs build Y" decisions so future sessions check the catalog
before re-searching. Seeded from memory.db facts and manually added entries.

Usage:
  parts-bin.py search "query"          # Search for relevant past decisions
  parts-bin.py add                     # Add a new decision (interactive or via flags)
  parts-bin.py list                    # List all entries
  parts-bin.py stats                   # Show catalog statistics
  parts-bin.py seed-from-memory        # Seed from memory.db recycler-related facts
  parts-bin.py export                  # Export as JSON to stdout

Each entry has:
  - id: unique slug
  - task: what was being built/solved
  - query: the search query that found the reusable code
  - found: what already existed in the codebase (reused as-is)
  - adapted: what was adapted from external sources (libs, repos, specs)
  - wrote_new: what was created from scratch
  - tags: searchable keywords
  - repo: which repo this applies to (or "general")
  - date: when the decision was made
  - session_id: which session produced this (if known)
  - confidence: how well the reuse worked (high/medium/low)
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

CATALOG_PATH = Path(os.environ.get("PARTS_BIN_PATH", str(Path.home() / ".factory" / "knowledge" / "parts-bin.json")))
PYTHON_EXE = sys.executable
MEMORY_DB = Path.home() / ".factory" / "memory.db"


def load_catalog() -> list[dict]:
    if not CATALOG_PATH.exists():
        return []
    try:
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_catalog(entries: list[dict]) -> None:
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def search(query: str, limit: int = 10) -> list[dict]:
    """Simple keyword-based search over the catalog."""
    entries = load_catalog()
    if not entries:
        return []
    query_lower = query.lower()
    query_terms = set(query_lower.split())

    scored: list[tuple[float, dict]] = []
    for entry in entries:
        searchable = " ".join([
            entry.get("task", ""),
            entry.get("query", ""),
            entry.get("found", ""),
            entry.get("adapted", ""),
            entry.get("wrote_new", ""),
            " ".join(entry.get("tags", [])),
            entry.get("repo", ""),
        ]).lower()

        score = 0.0
        for term in query_terms:
            if term in searchable:
                score += 1.0
            # Bonus for exact phrase match in task
            if term in entry.get("task", "").lower():
                score += 0.5
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:limit]]


def add_entry(
    task: str,
    found: str = "",
    adapted: str = "",
    wrote_new: str = "",
    query: str = "",
    tags: list[str] | None = None,
    repo: str = "general",
    session_id: str = "",
    confidence: str = "medium",
) -> dict:
    entries = load_catalog()
    entry_id = f"pb-{len(entries) + 1:04d}"
    entry = {
        "id": entry_id,
        "task": task,
        "query": query,
        "found": found,
        "adapted": adapted,
        "wrote_new": wrote_new,
        "tags": tags or [],
        "repo": repo,
        "date": datetime.now().isoformat(),
        "session_id": session_id,
        "confidence": confidence,
    }
    entries.append(entry)
    save_catalog(entries)
    return entry


def seed_from_memory() -> int:
    """Seed the catalog from memory.db facts related to recycler decisions."""
    if not MEMORY_DB.exists():
        print("memory.db not found, skipping seed", file=sys.stderr)
        return 0

    conn = sqlite3.connect(str(MEMORY_DB))
    count = 0

    # Look for facts that mention libraries, repos, reuse patterns
    keywords = ["found", "adapted", "wrote new", "reuse", "recycler", "library", "package", "helm chart", "terraform module"]
    for kw in keywords:
        rows = conn.execute(
            "SELECT content, metadata FROM facts WHERE category IN ('tool_usage','file_narrative','session_summary','narrative') AND content LIKE ? LIMIT 20",
            (f"%{kw}%",),
        ).fetchall()
        for content, metadata_json in rows:
            content_lower = content.lower()
            # Only seed if it looks like a recycler decision
            if not any(k in content_lower for k in ["found:", "adapted:", "wrote new:", "found -", "adapted -", "wrote new -"]):
                continue

            # Parse out FOUND/ADAPTED/WROTE NEW sections
            found = ""
            adapted = ""
            wrote_new = ""
            task = content[:120]

            # Try to extract sections
            for marker, target in [("FOUND:", "found"), ("ADAPTED:", "adapted"), ("WROTE NEW:", "wrote_new")]:
                if marker in content:
                    start = content.index(marker) + len(marker)
                    # Find next marker or end
                    end = len(content)
                    for next_marker in ["FOUND:", "ADAPTED:", "WROTE NEW:", "Skill effectiveness:", "Next improvement:"]:
                        if next_marker in content[start:]:
                            next_pos = content.index(next_marker, start)
                            if next_pos < end:
                                end = next_pos
                    target_val = content[start:end].strip()[:300]
                    if target == "found":
                        found = target_val
                    elif target == "adapted":
                        adapted = target_val
                    elif target == "wrote_new":
                        wrote_new = target_val

            if not found and not adapted and not wrote_new:
                continue

            # Check for duplicates
            existing = load_catalog()
            if any(e.get("task", "")[:60] == task[:60] for e in existing):
                continue

            add_entry(
                task=task,
                found=found,
                adapted=adapted,
                wrote_new=wrote_new,
                tags=[kw],
                repo="unknown",
                confidence="low",
            )
            count += 1

    conn.close()
    return count


def print_entry(entry: dict, verbose: bool = False) -> None:
    print(f"  [{entry['id']}] {entry['task'][:80]}")
    if verbose:
        if entry.get("found"):
            print(f"       FOUND: {entry['found'][:120]}")
        if entry.get("adapted"):
            print(f"       ADAPTED: {entry['adapted'][:120]}")
        if entry.get("wrote_new"):
            print(f"       WROTE NEW: {entry['wrote_new'][:120]}")
        print(f"       Tags: {', '.join(entry.get('tags', []))}")
        print(f"       Repo: {entry.get('repo', 'general')} | Confidence: {entry.get('confidence', 'medium')}")
        print(f"       Date: {entry.get('date', 'unknown')}")


def main():
    parser = argparse.ArgumentParser(description="Parts-bin catalog for recycler decisions")
    sub = parser.add_subparsers(dest="command")

    sp_search = sub.add_parser("search", help="Search for relevant past decisions")
    sp_search.add_argument("query", help="Search query")
    sp_search.add_argument("--limit", type=int, default=10)

    sp_add = sub.add_parser("add", help="Add a new decision")
    sp_add.add_argument("--task", required=True, help="What was being built/solved")
    sp_add.add_argument("--found", default="", help="What already existed")
    sp_add.add_argument("--adapted", default="", help="What was adapted from external sources")
    sp_add.add_argument("--wrote-new", default="", help="What was created from scratch")
    sp_add.add_argument("--query", default="", help="The search query that found the code")
    sp_add.add_argument("--tags", nargs="*", default=[], help="Searchable keywords")
    sp_add.add_argument("--repo", default="general", help="Which repo")
    sp_add.add_argument("--confidence", default="medium", choices=["high", "medium", "low"])

    sub.add_parser("list", help="List all entries")
    sub.add_parser("stats", help="Show catalog statistics")
    sub.add_parser("seed-from-memory", help="Seed from memory.db recycler facts")
    sub.add_parser("export", help="Export as JSON to stdout")

    args = parser.parse_args()

    if args.command == "search":
        results = search(args.query, args.limit)
        if not results:
            print(f"No parts-bin entries found for: {args.query}")
            print("This is a fresh query — no cached recycler decision exists yet.")
            return
        print(f"Parts-bin results for '{args.query}' ({len(results)} matches):")
        for entry in results:
            print_entry(entry, verbose=True)

    elif args.command == "add":
        entry = add_entry(
            task=args.task,
            found=args.found,
            adapted=args.adapted,
            wrote_new=args.wrote_new,
            query=args.query,
            tags=args.tags,
            repo=args.repo,
            confidence=args.confidence,
        )
        print(f"Added: [{entry['id']}] {entry['task'][:80]}")

    elif args.command == "list":
        entries = load_catalog()
        if not entries:
            print("Parts-bin catalog is empty. Use 'add' or 'seed-from-memory' to populate.")
            return
        print(f"Parts-bin catalog ({len(entries)} entries):")
        for entry in entries:
            print_entry(entry)

    elif args.command == "stats":
        entries = load_catalog()
        print(f"Parts-bin catalog statistics:")
        print(f"  Total entries: {len(entries)}")
        repos = {}
        for e in entries:
            r = e.get("repo", "general")
            repos[r] = repos.get(r, 0) + 1
        print(f"  By repo: {json.dumps(repos, indent=2)}")
        tags = {}
        for e in entries:
            for t in e.get("tags", []):
                tags[t] = tags.get(t, 0) + 1
        if tags:
            print(f"  Top tags: {json.dumps(dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]))}")

    elif args.command == "seed-from-memory":
        count = seed_from_memory()
        print(f"Seeded {count} entries from memory.db")

    elif args.command == "export":
        entries = load_catalog()
        print(json.dumps(entries, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
