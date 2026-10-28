#!/usr/bin/env python3
"""
Knowledge base query tool — lookup capabilities, services, credentials, deprecations, and error patterns.
Queries the kb_* tables in memory.db. Zero dependencies beyond Python stdlib + sqlite3.

Usage:
    python kb-query.py capability "<search>"    # Search action capability inventory
    python kb-query.py service "<search>"       # Search service listings
    python kb-query.py credential "<search>"    # Search credential references
    python kb-query.py deprecation              # List all deprecations
    python kb-query.py error                    # List error patterns
    python kb-query.py all "<search>"           # Search across all KB tables
"""
import sqlite3, sys, os
from pathlib import Path

MEMORY_DB = Path(os.environ.get("MEMORY_DB", Path.home() / ".factory" / "memory.db"))


def search_capabilities(query: str):
    db = sqlite3.connect(str(MEMORY_DB))
    terms = query.lower().split()
    rows = db.execute("SELECT action, primary_path, latency, fallback, notes, category FROM kb_capabilities").fetchall()
    results = []
    for row in rows:
        text = " ".join(str(c).lower() for c in row if c)
        score = sum(1 for t in terms if t in text)
        if score > 0:
            results.append((score, row))
    results.sort(key=lambda x: x[0], reverse=True)
    if results:
        print(f"{'ACTION':<35} {'PRIMARY PATH':<70} {'LAT':<8} {'CATEGORY'}")
        print("-" * 130)
        for score, (action, path, lat, fallback, notes, cat) in results[:10]:
            print(f"{action:<35} {path[:68]:<70} {lat:<8} {cat}")
    else:
        print(f"No capabilities matching '{query}'")
    db.close()


def search_services(query: str):
    db = sqlite3.connect(str(MEMORY_DB))
    terms = query.lower().split()
    rows = db.execute("SELECT name, machine, url, purpose, category FROM kb_services").fetchall()
    results = []
    for row in rows:
        text = " ".join(str(c).lower() for c in row if c)
        score = sum(1 for t in terms if t in text)
        if score > 0:
            results.append((score, row))
    results.sort(key=lambda x: x[0], reverse=True)
    if results:
        print(f"{'SERVICE':<25} {'MACHINE':<8} {'URL':<45} {'PURPOSE'}")
        print("-" * 120)
        for score, (name, machine, url, purpose, cat) in results[:10]:
            print(f"{name:<25} {machine:<8} {url[:43]:<45} {purpose}")
    else:
        print(f"No services matching '{query}'")
    db.close()


def search_credentials(query: str):
    db = sqlite3.connect(str(MEMORY_DB))
    terms = query.lower().split()
    rows = db.execute("SELECT what, doppler_project, doppler_config, key_name FROM kb_credentials").fetchall()
    results = []
    for row in rows:
        text = " ".join(str(c).lower() for c in row if c)
        score = sum(1 for t in terms if t in text)
        if score > 0:
            results.append((score, row))
    results.sort(key=lambda x: x[0], reverse=True)
    if results:
        print(f"{'WHAT':<30} {'DOPPLER PROJECT':<20} {'CONFIG':<10} {'KEY NAME'}")
        print("-" * 80)
        for score, (what, proj, conf, key) in results[:10]:
            print(f"{what:<30} {proj:<20} {conf:<10} {key}")
    else:
        print(f"No credentials matching '{query}'")
    db.close()


def list_deprecations():
    db = sqlite3.connect(str(MEMORY_DB))
    rows = db.execute("SELECT name, reason, superseded_by, archived_date FROM kb_deprecations ORDER BY archived_date DESC").fetchall()
    print(f"{'DEPRECATED':<30} {'SUPERSEDED BY':<45} {'DATE':<10} {'REASON'}")
    print("-" * 130)
    for name, reason, superseded, date in rows:
        print(f"{name:<30} {superseded[:43]:<45} {date:<10} {reason[:50]}")
    print(f"\n{len(rows)} deprecations")
    db.close()


def list_errors():
    db = sqlite3.connect(str(MEMORY_DB))
    rows = db.execute("SELECT pattern, sessions, action, last_seen FROM kb_error_patterns ORDER BY sessions DESC").fetchall()
    print(f"{'PATTERN':<20} {'SESSIONS':<10} {'ACTION'}")
    print("-" * 80)
    for pattern, sessions, action, last_seen in rows:
        print(f"{pattern:<20} {sessions:<10} {action}")
    db.close()


def search_all(query: str):
    print(f"=== Capabilities ===\n")
    search_capabilities(query)
    print(f"\n=== Services ===\n")
    search_services(query)
    print(f"\n=== Credentials ===\n")
    search_credentials(query)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    if cmd == "capability" or cmd == "cap":
        search_capabilities(q)
    elif cmd == "service" or cmd == "svc":
        search_services(q)
    elif cmd == "credential" or cmd == "cred":
        search_credentials(q)
    elif cmd == "deprecation" or cmd == "dep":
        list_deprecations()
    elif cmd == "error":
        list_errors()
    elif cmd == "all":
        search_all(q)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
