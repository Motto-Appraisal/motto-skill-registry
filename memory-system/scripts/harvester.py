"""Next-gen session harvester with structured fingerprinting.

Replaces regex heuristics with structured extraction:
1. Tool calls from JSONL assistant messages
2. Domain keyword extraction from user messages  
3. File path and service reference extraction
4. Error/failure detection

Fingerprint facts are embedded via nomic-embed-text and stored in memory.db
with session-level summaries for fast cross-session search.
"""
import json
import os
import re
import uuid
import sqlite3
import struct
import urllib.request
import math
from pathlib import Path
from datetime import datetime
from collections import Counter

MEMORY_DB = Path(os.environ.get("MEMORY_DB", Path.home() / ".factory" / "memory.db"))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text:latest"
# Colon-separated list of session JSONL dirs, optionally "label=path".
# Example: HARVEST_SESSION_DIRS="mac=~/Library/.../sessions:extra=/Volumes/backup/sessions"
_raw_dirs = os.environ.get("HARVEST_SESSION_DIRS", str(Path.home() / ".factory" / "sessions"))
SESSION_DIRS = []
for _entry in _raw_dirs.split(os.pathsep):
    _entry = _entry.strip()
    if not _entry:
        continue
    if "=" in _entry:
        _label, _path = _entry.split("=", 1)
    else:
        _path = _entry
        _label = Path(_entry).name or "sessions"
    SESSION_DIRS.append((_label.strip(), Path(_path).expanduser()))
BATCH_SIZE = 50

# Domain keywords that signal what a session is REALLY about
DOMAIN_KEYWORDS = [
    "stagehand", "playwright", "steel", "browserbase", "browser",
    "taxnet", "ntreis", "truetracts", "mls", "matrix", "clareity",
    "appraisal", "workfile", "artifact", "screenshot", "pdf",
    "comps", "property", "parcel", "county", "tax",
    "n8n", "tailscale", "tailnet", "coolify", "docker",
    "neo4j", "sourcebot", "hermes", "openhands",
    "sfrep", "doppler", "bitwarden", "grafana", "otel",
    "ollama", "mem0", "embeddings", "vector",
    "amc", "portal", "bid", "order", "intake",
    "sharepoint", "email", "loe", "credential", "windmill",
    "webhook", "automation", "download", "upload", "sync",
]

# Error-indicating patterns in assistant text — generic + domain-specific
ERROR_PATTERNS = [
    (r"(?:error|fail|blocked?|denied|disabled?)\s*(?::|in|at|by|with|on)\s*(.{10,120}?)(?:\.|$|\n)", "error"),
    (r"(?:403|401|500|502|503|timeout|ECONNREFUSED|ENOTFOUND)\s*(.{5,80}?)", "error"),
    (r"(?:couldn'?t|cannot|unable to|doesn'?t work)\s+(.{10,100}?)(?:\.|$|\n)", "error"),
    # Domain-specific: catch the real appraisal automation blockers
    (r"(?:Clareity|NTREIS)\s*(?:account|login|auth).{5,100}?(?:disabled|blocked|denied|403|failed)[^.]*\.?", "error"),
    (r"Google\s*secure.?browser.{5,100}?(?:block|denied|fail)[^.]*\.?", "error"),
    (r"(?:TaxNet|TrueTracts|NTREIS|MLS).{5,100}?(?:blocked|disabled|denied|fail(?:ed|ing)?|error|403|401)[^.]*\.?", "error"),
]


def get_embedding(text: str) -> list[float]:
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text[:1000]}).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA_URL}/api/embeddings", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())["embedding"]


def pack_vector(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def fingerprint_session(filepath: Path) -> dict | None:
    """Extract structured fingerprint from a session JSONL file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return None
    if len(lines) < 5:
        return None

    tool_calls = Counter()
    skills_used = set()
    user_keywords = Counter()
    assistant_errors = []
    file_paths = set()
    urls = set()
    message_count = 0
    user_msg_count = 0

    for line in lines:
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                continue

            t = record.get("type", "")

            if t == "message":
                message_count += 1
                msg = record.get("message", {})
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role", "")
                content = msg.get("content", [])
                if not isinstance(content, list):
                    continue

                for item in content:
                    if not isinstance(item, dict):
                        continue
                    item_type = item.get("type", "text")
                    item_text = item.get("text", "")

                    if item_type == "tool_use":
                        # Structured tool call
                        tool_name = item.get("name", "")
                        tool_calls[tool_name] += 1
                        if tool_name == "Skill":
                            inp = item.get("input", {})
                            if isinstance(inp, dict):
                                skill_name = inp.get("skill", "")
                                if skill_name:
                                    skills_used.add(skill_name)

                    elif item_type == "text" and isinstance(item_text, str):
                        # Skip system reminders
                        if item_text.startswith("<system-reminder"):
                            continue

                        if role == "user":
                            user_msg_count += 1
                            txt_lower = item_text.lower()
                            for kw in DOMAIN_KEYWORDS:
                                if kw in txt_lower:
                                    user_keywords[kw] += 1

                        elif role == "assistant" and len(item_text) > 20:
                            # Extract errors from assistant messages
                            for pattern, cat in ERROR_PATTERNS:
                                for m in re.finditer(pattern, item_text, re.IGNORECASE):
                                    err = m.group(0).strip()[:200]
                                    if len(err) > 10:
                                        assistant_errors.append(err)

                        # Extract file paths: any Windows drive letter path or Unix home/var path
                        for m in re.finditer(r'([A-Za-z]:[/\\][^\s"<>|]{5,200}|/(?:home|tmp|etc|var|usr|opt)/[^\s"<>|]{3,200})', item_text):
                            p = m.group(0).rstrip(".,;:)!}")
                            if 5 < len(p) < 200:
                                file_paths.add(p)

                        # Extract URLs
                        for m in re.finditer(r'https?://[^\s<>"{}|\\^`\[\]]+', item_text):
                            u = m.group(0).rstrip(".,;:)!}")
                            if len(u) > 15 and len(u) < 300:
                                urls.add(u)

        except json.JSONDecodeError:
            continue

    if message_count < 5:
        return None

    # Build facts from the fingerprint
    facts = []

    # Tool usage facts
    for tool, count in tool_calls.most_common(30):
        facts.append(("tool_usage", f"tool:{tool}(x{count})"))

    # Skill usage facts
    for skill in sorted(skills_used)[:20]:
        facts.append(("skill_used", f"skill:{skill}"))

    # Domain keyword facts (top 15)
    for kw, count in user_keywords.most_common(15):
        facts.append(("domain", f"keyword:{kw}(x{count})"))

    # Error facts (top 5)
    for err in assistant_errors[:5]:
        facts.append(("error", f"error:{err[:150]}"))

    # File path facts (top 10, prioritize artifact/workfile paths)
    artifact_paths = [p for p in file_paths if any(k in p.lower() for k in ("workfile", "wf_", "motto", "appraisal", "artifact"))]
    other_paths = [p for p in file_paths if p not in artifact_paths]
    for fp in sorted(artifact_paths)[:8]:
        facts.append(("file", f"file:{fp[:180]}"))
    for fp in sorted(other_paths)[:5]:
        facts.append(("file", f"file:{fp[:180]}"))

    # URL facts (top 5)
    for u in sorted(urls)[:5]:
        facts.append(("url", f"url:{u[:180]}"))

    # Session metadata fact
    size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 1)
    facts.append(("session_meta", f"session:{filepath.stem} size={size_mb}MB msgs={message_count} user_msgs={user_msg_count}"))

    # Artifact location facts: store exact paths where workfiles/artifacts live
    artifact_dirs = set()
    for fp in artifact_paths:
        fp_clean = fp.rstrip("`'\",;")
        # Extract WF_{slug} directory or Motto-Workfiles parent
        for m in re.finditer(r'(?:Desktop|workfiles|WF_)[^\s"<>|]*Workfiles[^\s"<>|]*', fp_clean, re.IGNORECASE):
            artifact_dirs.add(m.group(0)[:200])
        for m in re.finditer(r'([A-Za-z]:[/\\][^\s"<>|]*WF_[^\s"<>|]{5,100})', fp_clean, re.IGNORECASE):
            artifact_dirs.add(m.group(0)[:200])
    for ad in sorted(artifact_dirs)[:5]:
        facts.append(("artifact_location", f"artifact_location:{ad}"))

    # Compound blocker facts: combine domain keywords with errors
    blocker_keywords = {"ntreis", "clareity", "blocked", "disabled", "denied", "truetracts", "google", "secure-browser"}
    blocker_kws_found = {kw for kw in user_keywords if kw in blocker_keywords}
    if blocker_kws_found and assistant_errors:
        # Find the most specific error
        domain_errors = [e for e in assistant_errors if any(kw in e.lower() for kw in blocker_keywords)]
        if domain_errors:
            facts.append(("blocker", f"blocker:{domain_errors[0][:180]}"))
        elif assistant_errors:
            facts.append(("blocker", f"blocker:{assistant_errors[0][:180]}"))

    # Workflow inventory fact: detect multiple workflow types, not just browser automation
    WORKFLOW_PATTERNS = {
        "browser_automation": {"stagehand", "playwright", "steel", "browserbase"},
        "portal_scraping": {"taxnet", "ntreis", "truetracts", "mls", "matrix", "clareity"},
        "sharepoint_integration": {"sharepoint"},
        "email_intake": {"email", "intake"},
        "credential_rotation": {"credential", "stagehand"},
        "n8n_workflow": {"n8n", "webhook", "automation"},
        "pdf_download": {"pdf", "download", "taxnet"},
        "windmill_deployment": {"windmill", "coolify"},
    }
    for wf_type, keywords in WORKFLOW_PATTERNS.items():
        found = {kw for kw in user_keywords if kw in keywords}
        if len(found) >= 2 or (len(found) >= 1 and wf_type == "email_intake"):
            facts.append(("workflow", f"workflow:{wf_type} domains={','.join(sorted(found)[:6])}"))

    # Session summary for structured search
    top_keywords = [kw for kw, _ in user_keywords.most_common(8)]
    top_tools = [t for t, _ in tool_calls.most_common(5)]
    summary = {
        "session_id": filepath.stem,
        "size_mb": size_mb,
        "message_count": message_count,
        "user_msg_count": user_msg_count,
        "top_tools": top_tools,
        "top_keywords": top_keywords,
        "skills_used": list(skills_used)[:10],
        "error_count": len(assistant_errors),
        "file_count": len(file_paths),
    }

    return {
        "session_id": filepath.stem,
        "facts": facts,
        "summary": summary,
    }


def ensure_db():
    db = sqlite3.connect(str(MEMORY_DB))
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS facts (
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now')),
            source TEXT DEFAULT 'harvest',
            status TEXT DEFAULT 'live',
            relevance INTEGER DEFAULT 1,
            distilled INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS embeddings (
            fact_id TEXT PRIMARY KEY REFERENCES facts(id) ON DELETE CASCADE,
            vector BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS session_summaries (
            session_id TEXT PRIMARY KEY,
            summary_json TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            source TEXT DEFAULT 'harvest'
        );
        CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
        CREATE INDEX IF NOT EXISTS idx_facts_created ON facts(created_at);
    """)
    db.commit()
    return db


def harvest_directory(sessions_dir: Path, source_label: str, limit: int = 500, incremental: bool = False, cooldown_minutes: int = 0):
    """Harvest fingerprints from a sessions directory with embeddings.
    If incremental=True, skip sessions already in session_summaries.
    If cooldown_minutes > 0, skip files modified within the last N minutes (session still active)."""
    db = ensure_db()
    
    existing_sessions = set()
    if incremental:
        rows = db.execute("SELECT session_id FROM session_summaries").fetchall()
        existing_sessions = {r[0] for r in rows}
    
    now = datetime.now()
    
    files = sorted(sessions_dir.rglob("*.jsonl"), key=lambda f: -os.path.getsize(f))
    session_count = 0
    fact_count = 0
    pending_embeds = []
    skipped = 0
    cooled = 0

    for fpath in files:
        if incremental and fpath.stem in existing_sessions:
            skipped += 1
            continue
        if cooldown_minutes > 0:
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
            age_minutes = (now - mtime).total_seconds() / 60
            if age_minutes < cooldown_minutes:
                cooled += 1
                continue
        if session_count >= limit:
            break
        result = fingerprint_session(fpath)
        if not result or not result["facts"]:
            continue

        sid = result["session_id"]

        # Store session summary
        db.execute(
            "INSERT OR REPLACE INTO session_summaries (session_id, summary_json, source) VALUES (?, ?, ?)",
            (sid, json.dumps(result["summary"]), source_label)
        )

        # Store facts
        for category, fact_text in result["facts"]:
            fact_id = f"{source_label}-{sid}-{fact_count}"
            metadata = json.dumps({
                "session_id": sid,
                "source": source_label,
                "harvested_at": datetime.now().isoformat()
            })
            db.execute(
                "INSERT OR REPLACE INTO facts (id, category, content, metadata, source) VALUES (?, ?, ?, ?, ?)",
                (fact_id, category, fact_text, metadata, source_label)
            )
            pending_embeds.append((fact_id, fact_text))
            fact_count += 1

            if len(pending_embeds) >= BATCH_SIZE:
                _embed_batch(db, pending_embeds)
                pending_embeds = []

        session_count += 1
        if session_count % 20 == 0:
            print(f"  [{source_label}] {session_count} sessions, {fact_count} facts...")
        # Commit every 50 sessions to survive timeouts
        if session_count % 50 == 0:
            db.commit()

    if pending_embeds:
        _embed_batch(db, pending_embeds)

    db.commit()
    db.close()
    parts = [f"{session_count} sessions, {fact_count} facts"]
    if skipped:
        parts.append(f"{skipped} skipped")
    if cooled:
        parts.append(f"{cooled} still-active (cooldown)")
    print(f"  [{source_label}] Done: {', '.join(parts)}")
    return session_count, fact_count


def _embed_batch(db: sqlite3.Connection, batch: list[tuple[str, str]]):
    for fact_id, text in batch:
        try:
            vec = get_embedding(text)
            db.execute(
                "INSERT OR REPLACE INTO embeddings (fact_id, vector) VALUES (?, ?)",
                (fact_id, pack_vector(vec))
            )
        except Exception:
            pass


def search(query: str, top_k: int = 10) -> list[dict]:
    """Hybrid search: text overlap for specifics + embedding for concepts.
    
    If query contains specific terms (file paths, tool names, domain names),
    text overlap gets 70% weight. Otherwise embedding dominates.
    """
    db = ensure_db()
    results = []
    query_lower = query.lower()
    query_terms = set(query_lower.split())
    
    # Determine if this is a specific or conceptual query
    specific_indicators = ["wf_", "workfile", "desktop", "stagehand", "playwright", "steel",
                           "taxnet", "ntreis", "truetracts", "clareity", "neo4j", "sourcebot",
                           "hermes", "doppler", "ollama", "grafana", "docker"]
    is_specific = any(ind in query_lower for ind in specific_indicators)
    
    try:
        qvec = get_embedding(query)
        rows = db.execute("""
            SELECT e.fact_id, e.vector, f.category, f.content, f.metadata, f.created_at, f.status, f.relevance
            FROM embeddings e JOIN facts f ON e.fact_id = f.id
            WHERE f.status = 'live' OR f.status IS NULL
        """).fetchall()
        
        for row in rows:
            # Embedding score
            vec = list(struct.unpack(f"{len(row[1])//4}f", row[1]))
            dot = sum(a * b for a, b in zip(qvec, vec))
            na = math.sqrt(sum(x * x for x in qvec))
            nb = math.sqrt(sum(x * x for x in vec))
            emb_score = dot / (na * nb) if na and nb else 0
            
            # Text overlap score: how many query terms appear in the fact?
            fact_lower = row[3].lower()
            if query_terms:
                text_score = sum(1 for t in query_terms if t in fact_lower) / len(query_terms)
            else:
                text_score = 0
            
            # Hybrid: specific queries favor text, conceptual favors embedding
            if is_specific:
                score = text_score * 0.7 + emb_score * 0.3
            else:
                score = text_score * 0.3 + emb_score * 0.7
            
            # Category boosts (multipliers only — no floors that override hybrid)
            if row[6] == "superseded":
                score *= 0.3
            elif row[2] == "current_status":
                score *= 1.2
            elif row[2] == "bottleneck":
                score *= 1.15
            elif row[2] == "narrative":
                score *= 1.1
            elif row[2] == "parent_link":
                score *= 1.15
            elif row[2] == "code_graph":
                score *= 1.1
            elif row[2] == "knowledge":
                score *= 1.15
            elif row[2] == "recidivism":
                score *= 1.2
            elif row[2] == "pipeline_arch":
                score *= 1.1
            
            # Relevance boost
            try:
                relevance = int(row[7]) if row[7] else 1
                if relevance > 1:
                    score *= (1 + (relevance - 1) * 0.1)
            except:
                pass
            
            results.append({
                "fact_id": row[0], "category": row[2], "content": row[3],
                "metadata": row[4], "created_at": row[5], "score": score,
                "status": row[6], "match_type": "hybrid"
            })
        results.sort(key=lambda x: x["score"], reverse=True)
    except Exception:
        pass
    
    # Text fallback
    if not results:
        rows = db.execute(
            """SELECT id, category, content, metadata, created_at, status FROM facts 
               WHERE content LIKE ? AND (status='live' OR status IS NULL)
               ORDER BY created_at DESC LIMIT ?""",
            (f"%{query}%", top_k)
        ).fetchall()
        results = [{"fact_id": r[0], "category": r[1], "content": r[2], "metadata": r[3],
                     "created_at": r[4], "score": 0.5, "match_type": "text", "status": r[5]} for r in rows]
    
    # Post-process: deduplicate and enrich
    
    # 1. Remove noise: facts shorter than 20 chars or pure template slugs
    results = [r for r in results if len(r["content"]) > 20 and "{slug}" not in r["content"]]
    
    # 2. Deduplicate: keep highest-scoring version of near-identical content
    seen_content = {}
    deduped = []
    for r in results:
        key = r["content"].lower()[:80].strip()
        if key in seen_content:
            if r["score"] > seen_content[key]["score"]:
                seen_content[key] = r
        else:
            seen_content[key] = r
    results = sorted(seen_content.values(), key=lambda x: x["score"], reverse=True)
    
    # 3. Enrich: add category label and relevance indicator
    for r in results:
        cat_labels = {
            "current_status": "[STATE]", "bottleneck": "[LESSON]", "knowledge": "[KNOWLEDGE]",
            "narrative": "[SESSION]", "error": "[ERROR]", "blocker": "[BLOCKER]",
            "artifact_location": "[PATH]", "code_graph": "[REPO]", "workflow": "[FLOW]",
            "recidivism": "[RECUR]", "file": "[FILE]", "url": "[URL]",
        }
        r["label"] = cat_labels.get(r["category"], f"[{r['category']}]")
    
    db.close()
    return results[:top_k]


def co_occurrence_search(query: str, top_k: int = 10) -> list[dict]:
    """Find sessions where multiple query terms co-occur as keywords.
    Solves the 'NTREIS + blocked + Clareity' gap by finding sessions
    that contain ALL the query terms as keywords, not just one."""
    db = ensure_db()
    terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 2]
    if len(terms) < 2:
        return search(query, top_k)  # Fall back to regular search

    # Find sessions that have ALL terms as keywords
    placeholders = ",".join("?" for _ in terms)
    like_clauses = " OR ".join("f.content LIKE ?" for _ in terms)
    params = [f"%{t}%" for t in terms] * 2  # Once for domain check, once for like

    # Query: find facts from sessions where ALL query terms appear as keywords
    rows = db.execute(f"""
        SELECT f.id, f.category, f.content, f.metadata, f.created_at,
               (SELECT COUNT(DISTINCT f2.content) FROM facts f2
                WHERE f2.metadata = f.metadata AND ({like_clauses}))
               as term_count
        FROM facts f
        WHERE ({like_clauses})
        ORDER BY term_count DESC, f.created_at DESC
        LIMIT ?
    """, params + [top_k * 2]).fetchall()

    results = []
    session_scores = {}
    for row in rows:
        sid = ""
        try:
            meta = json.loads(row[3])
            sid = meta.get("session_id", "")
        except:
            pass
        if sid:
            session_scores[sid] = session_scores.get(sid, 0) + 1

        results.append({
            "fact_id": row[0], "category": row[1], "content": row[2],
            "metadata": row[3], "created_at": row[4],
            "score": 0.5 + (row[5] * 0.15),  # Higher score for more matching terms
            "match_type": "co_occurrence",
            "session_id": sid,
        })

    # Boost sessions that match ALL terms
    max_terms = len(terms)
    for r in results:
        sid = r.get("session_id", "")
        if session_scores.get(sid, 0) >= max_terms:
            r["score"] += 0.3  # Full match bonus

    # Sort by score, deduplicate by session
    seen_sessions = set()
    deduped = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        sid = r.get("session_id", "")
        if sid and sid not in seen_sessions:
            seen_sessions.add(sid)
            deduped.append(r)
            if len(deduped) >= top_k:
                break

    # Add regular search results as fallback
    if len(deduped) < top_k:
        regular = search(query, top_k - len(deduped))
        for r in regular:
            r["match_type"] = "embedding_fallback"
        deduped.extend(regular)

    db.close()
    return deduped[:top_k]


def build_workflow_inventory() -> str:
    """Auto-generate a portal workflow inventory from session summaries. Free, no LLM."""
    db = ensure_db()
    rows = db.execute("""
        SELECT f.content FROM facts f
        WHERE f.category IN ('workflow', 'blocker', 'artifact_location')
        ORDER BY f.created_at DESC
        LIMIT 100
    """).fetchall()

    workflows = [r[0] for r in rows if r[0].startswith("workflow:")]
    blockers = [r[0] for r in rows if r[0].startswith("blocker:")]
    locations = [r[0] for r in rows if r[0].startswith("artifact_location:")]

    # Count unique workflow domains
    domains = set()
    for w in workflows:
        for m in re.finditer(r'domains=([^)]+)', w):
            domains.update(m.group(1).split(","))

    parts = ["=== PORTAL AUTOMATION WORKFLOW INVENTORY ==="]
    parts.append(f"Workflows detected: {len(workflows)} across domains: {', '.join(sorted(domains))}")
    parts.append("")
    if locations:
        parts.append("Artifact locations:")
        for l in sorted(set(locations))[:8]:
            parts.append(f"  {l}")
    parts.append("")
    if blockers:
        parts.append("Known blockers:")
        for b in sorted(set(blockers))[:10]:
            parts.append(f"  {b}")
    parts.append("")

    inventory = "\n".join(parts)
    db.close()
    return inventory


def get_stats():
    db = ensure_db()
    facts = db.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    embeds = db.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
    sources = dict(db.execute("SELECT source, COUNT(*) FROM facts GROUP BY source").fetchall())
    cats = [{"category": r[0], "count": r[1]} for r in
            db.execute("SELECT category, COUNT(*) FROM facts GROUP BY category ORDER BY COUNT(*) DESC LIMIT 15").fetchall()]
    summaries = db.execute("SELECT COUNT(*) FROM session_summaries").fetchone()[0]
    db.close()
    return {
        "total_facts": facts,
        "total_embeddings": embeds,
        "sources": sources,
        "categories": cats,
        "session_summaries": summaries,
    }


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"

    if cmd == "harvest":
        scope = sys.argv[2] if len(sys.argv) > 2 else "all"
        incremental = "--incr" in sys.argv or "--incremental" in sys.argv
        # Parse --cooldown N flag
        cooldown = 0
        for i, a in enumerate(sys.argv):
            if a == "--cooldown" and i + 1 < len(sys.argv):
                try:
                    cooldown = int(sys.argv[i + 1])
                except ValueError:
                    pass
        
        # Filter out flags to get limit
        args = [a for a in sys.argv[3:] if not a.startswith("--")]
        limit = int(args[0]) if args else 500
        
        for label, sessions_dir in SESSION_DIRS:
            if scope in ("all", label) and sessions_dir.exists():
                print(f"Harvesting {label} sessions ({sessions_dir}){' [incremental]' if incremental else ''}{' [cooldown=' + str(cooldown) + 'm]' if cooldown else ''}...")
                harvest_directory(sessions_dir, label, limit, incremental, cooldown)

    elif cmd == "search":
        query = " ".join(sys.argv[2:])
        results = search(query, 15)
        print(f"Search: '{query}' -> {len(results)} results\n")
        for r in results:
            print(f"[{r['score']:.3f}] {r.get('label', r['category'])} {r['content'][:150]}")

    elif cmd == "fingerprint":
        # Fingerprint a single session for inspection
        filepath = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        if filepath and filepath.exists():
            result = fingerprint_session(filepath)
            if result:
                print(f"\nSession: {result['session_id']}")
                print(f"\nSummary:")
                for k, v in result["summary"].items():
                    print(f"  {k}: {v}")
                print(f"\nFacts ({len(result['facts'])}):")
                for cat, text in result["facts"][:30]:
                    print(f"  [{cat}] {text[:120]}")
            else:
                print("No facts extracted.")
        else:
            print("Usage: python harvester.py fingerprint <session.jsonl>")

    elif cmd == "stats":
        stats = get_stats()
        print(f"Facts: {stats['total_facts']}, Embeddings: {stats['total_embeddings']}")
        print(f"Session summaries: {stats['session_summaries']}")
        print(f"Sources: {stats['sources']}")
        print("Categories:")
        for c in stats["categories"]:
            print(f"  {c['category']}: {c['count']}")
