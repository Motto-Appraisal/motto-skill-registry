#!/usr/bin/env python3
r"""Universal done-verification script.

Run before declaring any task complete. Checks the task type, runs the
minimum verification steps, records a `verification` fact, and prints a
summary the droid can include in its final response.

Usage:
    python verify-done.py --task-type code --repo-path C:\path\to\repo
    python verify-done.py --task-type infra --service grafana-otel
    python verify-done.py --task-type config --file C:\path\to\config.json
    python verify-done.py --task-type research --question "..." --answer "..."
    python verify-done.py --task-type file --file C:\path\to\file.txt
"""
import argparse
import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

MEMORY_DB = Path(os.environ.get("MEMORY_DB", Path.home() / ".factory" / "memory.db"))
OTEL_ENDPOINT = os.environ.get("OTEL_ENDPOINT", "http://localhost:4318")
GRAFANA_URL = os.environ.get("GRAFANA_URL", "http://localhost:3000")
TEMPO_MCP_URL = os.environ.get("TEMPO_MCP_URL", "http://localhost:3200")


def ensure_db():
    db = sqlite3.connect(str(MEMORY_DB))
    db.execute("PRAGMA journal_mode=WAL")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS facts (
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now')),
            source TEXT DEFAULT 'verify-done',
            status TEXT DEFAULT 'live'
        );
        CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
        CREATE INDEX IF NOT EXISTS idx_facts_created ON facts(created_at);
    """)
    return db


def record_verification(checks, passed, failed, summary):
    db = ensure_db()
    fact_id = f"verification-{datetime.now().isoformat()}"
    content = f"verification:{'pass' if not failed else 'fail'} | {summary}"
    metadata = json.dumps({
        "checks": checks,
        "passed": passed,
        "failed": failed,
        "verified_at": datetime.now().isoformat(),
    })
    db.execute(
        "INSERT OR REPLACE INTO facts (id, category, content, metadata, source) VALUES (?, ?, ?, ?, ?)",
        (fact_id, "verification", content, metadata, "verify-done")
    )
    db.commit()
    db.close()


def run_cmd(cmd, cwd=None, timeout=60):
    """Run a shell command and return a structured result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip()[:500],
            "stderr": result.stderr.strip()[:500],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout", "stdout": "", "stderr": ""}
    except Exception as e:
        return {"ok": False, "error": str(e), "stdout": "", "stderr": ""}


def detect_package_manager(repo_path: Path) -> str | None:
    if (repo_path / "package.json").exists():
        return "npm"
    if (repo_path / "pyproject.toml").exists() or (repo_path / "setup.py").exists():
        return "python"
    if (repo_path / "Cargo.toml").exists():
        return "cargo"
    if (repo_path / "go.mod").exists():
        return "go"
    return None


# Executables we recognize as real verification runners. A backticked token
# only counts as a command when its first word is one of these AND that word
# resolves on PATH. This prevents prose tokens (e.g. `needs-operator`,
# `claude-task`, `tests/`) from being mis-parsed and run as shell commands.
KNOWN_RUNNERS = {
    "pytest", "ruff", "black", "mypy", "flake8", "pylint", "tox", "nox",
    "python", "python3", "poetry", "uv",
    "npm", "pnpm", "yarn", "npx", "bun", "deno", "node",
    "eslint", "prettier", "jest", "vitest", "tsc",
    "cargo", "go", "make", "gradle", "mvn", "dotnet",
}

# A verification command must express test/lint/type-check intent. This keeps
# setup/install/build commands (e.g. `pip install ...`, `npm run build`) out of
# the verification set.
VERIFY_INTENT = (
    "test", "pytest", "lint", "ruff", "black", "mypy", "flake8", "pylint",
    "check", "typecheck", "tsc", "clippy", "vet", "eslint", "prettier",
    "jest", "vitest", "nox", "tox",
)

# Verification must be READ-ONLY. Reject any command that rewrites source in
# place (auto-fixers/formatters). A bare formatter (e.g. `black .`) also writes,
# so formatters are only accepted in check/diff mode.
WRITE_FLAGS = ("--fix", "--fix-only", "--write", "--in-place")
FORMATTERS = {"black", "isort", "prettier", "yapf", "autopep8"}


# Python tools commonly invoked via `python -m <tool>` when not on PATH.
PY_MODULE_TOOLS = {"pytest", "ruff", "black", "mypy", "flake8", "pylint"}


def _resolve_runner(cmd: str, tokens: list[str]) -> str | None:
    """Return a runnable command string, rewriting Python tools to
    `python -m <tool>` when the bare executable isn't on PATH. Returns None
    when the command can't be run here (so it's skipped, not falsely failed)."""
    import importlib.util
    import shutil

    runner = tokens[0]
    if shutil.which(runner) is not None:
        return cmd
    if runner.lower() in PY_MODULE_TOOLS:
        py = sys.executable or shutil.which("python") or shutil.which("python3")
        if py and importlib.util.find_spec(runner.lower()) is not None:
            rest = cmd[len(runner):].lstrip()
            return f'"{py}" -m {runner.lower()} {rest}'.rstrip()
    return None


def _normalize_command(raw: str) -> tuple[str, str] | None:
    """Return (first_token, command) if `raw` looks like a runnable
    verification command whose runner is a known, installed tool; else None."""
    cmd = raw.strip().strip("$").strip()
    if not cmd or len(cmd) > 200 or "\n" in cmd:
        return None
    # Skip compound commands; a partial runner rewrite would be wrong.
    if any(op in cmd for op in ("&&", "||", ";", "|")):
        return None
    tokens = cmd.split()
    if len(tokens) < 2:
        # Bare single tokens are almost never a verify command (they're
        # usually names/paths in prose). Require at least a runner + arg.
        return None
    runner = tokens[0].lower()
    if runner not in KNOWN_RUNNERS:
        return None
    lowered = cmd.lower()
    if "install" in lowered:
        return None
    # Never run mutating commands: auto-fixers or bare formatters rewrite source.
    if any(flag in lowered.split() for flag in WRITE_FLAGS):
        return None
    if runner in FORMATTERS and not ("--check" in lowered or "--diff" in lowered):
        return None
    if not any(kw in lowered for kw in VERIFY_INTENT):
        return None
    resolved = _resolve_runner(cmd, tokens)
    if resolved is None:
        # Can't run it here; skip rather than emit a false failure.
        return None
    return runner, resolved


def discover_project_commands(repo_path: Path) -> list[tuple[str, str]]:
    """Discover verification commands from project CLAUDE.md or AGENTS.md.

    Prefers fenced code blocks; falls back to inline-backtick tokens. A
    candidate only qualifies when its first token is a known runner that is
    installed on PATH (see `_normalize_command`), so descriptive prose in
    backticks is never executed.

    Returns list of (label, command) tuples.
    """
    import re

    cmd_re = re.compile(r"`([^`]{3,200})`")
    fence_re = re.compile(r"^```")

    for filename in ("CLAUDE.md", "AGENTS.md"):
        filepath = repo_path / filename
        if not filepath.exists():
            continue
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            continue

        commands: list[tuple[str, str]] = []
        seen: set[str] = set()

        def _add(raw: str) -> None:
            # Split shell-compound lines so each verification tool is checked
            # independently (e.g. "ruff check . && black --check .").
            for segment in re.split(r"&&|\|\||;", raw):
                norm = _normalize_command(segment)
                if not norm:
                    continue
                _, cmd = norm
                if cmd in seen:
                    continue
                seen.add(cmd)
                commands.append((f"project: {cmd[:60]}", cmd))

        # 1) Fenced code blocks: take each line inside ```...``` blocks.
        in_fence = False
        for line in content.split("\n"):
            if fence_re.match(line.strip()):
                in_fence = not in_fence
                continue
            if in_fence:
                _add(line)

        # 2) Inline backticks as a fallback when no fenced commands found.
        if not commands:
            for line in content.split("\n"):
                for m in cmd_re.finditer(line):
                    _add(m.group(1))

        if commands:
            return commands[:5]

    return []


def verify_code(repo_path: Path, quick: bool = False):
    checks = []
    pm = detect_package_manager(repo_path)

    # First, try to discover project-level commands from CLAUDE.md/AGENTS.md
    project_cmds = discover_project_commands(repo_path)
    
    if project_cmds:
        for label, cmd in project_cmds:
            checks.append((label, run_cmd(cmd, cwd=repo_path, timeout=120)))
    elif pm == "npm":
        checks.append(("npm test", run_cmd("npm test", cwd=repo_path, timeout=120)))
        checks.append(("npm run lint", run_cmd("npm run lint", cwd=repo_path, timeout=60)))
        if not quick:
            checks.append(("npm run typecheck", run_cmd("npm run typecheck", cwd=repo_path, timeout=60)))
    elif pm == "python":
        import shutil
        py = sys.executable or shutil.which("python") or shutil.which("python3") or "python"
        pytest_cmd = "pytest" if shutil.which("pytest") else f'"{py}" -m pytest'
        ruff_cmd = "ruff check ." if shutil.which("ruff") else f'"{py}" -m ruff check .'
        checks.append(("pytest", run_cmd(pytest_cmd, cwd=repo_path, timeout=120)))
        checks.append(("ruff check .", run_cmd(ruff_cmd, cwd=repo_path, timeout=60)))
    elif pm == "cargo":
        checks.append(("cargo test", run_cmd("cargo test", cwd=repo_path, timeout=180)))
        checks.append(("cargo clippy", run_cmd("cargo clippy -- -D warnings", cwd=repo_path, timeout=120)))
    elif pm == "go":
        checks.append(("go test ./...", run_cmd("go test ./...", cwd=repo_path, timeout=120)))
        checks.append(("go vet ./...", run_cmd("go vet ./...", cwd=repo_path, timeout=60)))
    else:
        checks.append(("repo exists", {"ok": True, "stdout": str(repo_path)}))

    return checks


def verify_config(file_path: Path, service: str | None = None):
    checks = []
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            json.loads(content)
            checks.append(("json syntax", {"ok": True, "stdout": "valid JSON"}))
        except json.JSONDecodeError as e:
            checks.append(("json syntax", {"ok": False, "stderr": str(e)}))
        except Exception as e:
            checks.append(("file readable", {"ok": False, "stderr": str(e)}))
    else:
        checks.append(("file exists", {"ok": False, "stderr": f"{file_path} not found"}))

    if service:
        # Check if the service is running via Docker or local process
        docker_result = run_cmd(f'docker ps --filter "name={service}" --format "{{{{.Names}}}}"')
        if docker_result["stdout"]:
            checks.append(("service running", {"ok": True, "stdout": docker_result["stdout"]}))
        else:
            checks.append(("service running", {"ok": False, "stderr": f"{service} not found in docker ps"}))

    return checks


def verify_infra(service: str | None = None):
    checks = []
    # OTEL collector health
    otel = run_cmd(f'curl -s -o /dev/null -w "%{{http_code}}" {OTEL_ENDPOINT}/v1/metrics', timeout=10)
    checks.append(("otel reachable", {"ok": otel.get("stdout") in ("200", "202", "204"), "stdout": otel.get("stdout", "")}))

    # Grafana health
    grafana = run_cmd(f'curl -s -o /dev/null -w "%{{http_code}}" {GRAFANA_URL}/api/health', timeout=10)
    checks.append(("grafana reachable", {"ok": grafana.get("stdout") == "200", "stdout": grafana.get("stdout", "")}))

    if service:
        docker_result = run_cmd(f'docker ps --filter "name={service}" --format "{{{{.Names}}}}"')
        checks.append(("service container", {"ok": bool(docker_result.get("stdout")), "stdout": docker_result.get("stdout", "")}))

    return checks


def verify_research(question: str, answer: str, sources: list[str] | None = None):
    checks = []
    # Basic fit check: does the answer contain terms from the question?
    q_terms = set(question.lower().split())
    a_terms = set(answer.lower().split())
    overlap = len(q_terms & a_terms)
    fit = overlap >= max(1, len(q_terms) * 0.2)
    checks.append(("answer fit", {"ok": fit, "stdout": f"{overlap}/{len(q_terms)} question terms in answer"}))

    if sources:
        checks.append(("sources cited", {"ok": len(sources) > 0, "stdout": f"{len(sources)} sources"}))
    else:
        checks.append(("sources cited", {"ok": False, "stderr": "no sources provided"}))

    return checks


def verify_file(file_path: Path):
    checks = []
    if file_path.exists():
        checks.append(("file exists", {"ok": True, "stdout": str(file_path)}))
        try:
            size = file_path.stat().st_size
            checks.append(("file readable", {"ok": size > 0, "stdout": f"{size} bytes"}))
        except Exception as e:
            checks.append(("file readable", {"ok": False, "stderr": str(e)}))
    else:
        checks.append(("file exists", {"ok": False, "stderr": f"{file_path} not found"}))
    return checks


def format_report(checks):
    passed = []
    failed = []
    for name, result in checks:
        if result.get("ok"):
            passed.append(f"  ✅ {name}: {result.get('stdout', '')}".rstrip())
        else:
            failed.append(f"  ❌ {name}: {result.get('stderr', result.get('error', 'failed'))}".rstrip())
    return passed, failed


def main():
    parser = argparse.ArgumentParser(description="Verify a task before declaring it done.")
    parser.add_argument("--task-type", required=True, choices=["code", "config", "infra", "research", "file"])
    parser.add_argument("--repo-path", type=Path)
    parser.add_argument("--service", type=str)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--question", type=str)
    parser.add_argument("--answer", type=str)
    parser.add_argument("--sources", nargs="*", default=[])
    parser.add_argument("--quick", action="store_true", help="Skip slower checks like typecheck.")
    args = parser.parse_args()

    if args.task_type == "code" and not args.repo_path:
        print("Error: --repo-path required for code tasks", file=sys.stderr)
        sys.exit(1)
    if args.task_type == "config" and not args.file:
        print("Error: --file required for config tasks", file=sys.stderr)
        sys.exit(1)
    if args.task_type == "infra" and not args.service:
        # service is optional for infra
        pass
    if args.task_type == "research" and (not args.question or not args.answer):
        print("Error: --question and --answer required for research tasks", file=sys.stderr)
        sys.exit(1)
    if args.task_type == "file" and not args.file:
        print("Error: --file required for file tasks", file=sys.stderr)
        sys.exit(1)

    if args.task_type == "code":
        checks = verify_code(args.repo_path, quick=args.quick)
    elif args.task_type == "config":
        checks = verify_config(args.file, service=args.service)
    elif args.task_type == "infra":
        checks = verify_infra(service=args.service)
    elif args.task_type == "research":
        checks = verify_research(args.question, args.answer, args.sources)
    elif args.task_type == "file":
        checks = verify_file(args.file)
    else:
        checks = []

    passed, failed = format_report(checks)
    summary = f"{len(passed)} passed, {len(failed)} failed"
    record_verification([name for name, _ in checks], passed, failed, summary)

    print("Verification Report")
    print("=" * 50)
    print(f"Task type: {args.task_type}")
    print(summary)
    if passed:
        print("\n".join(passed))
    if failed:
        print("\n".join(failed))

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
