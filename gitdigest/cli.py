import subprocess
import re
from collections import defaultdict
from datetime import datetime
import click
from rich.console import Console

console = Console()

TYPES = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "refactor": "Refactoring",
    "docs": "Documentation",
    "test": "Tests",
    "chore": "Chores",
    "perf": "Performance",
    "ci": "CI",
}

COMMIT_RE = re.compile(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<msg>.+)$")


def get_commits(since: str | None) -> list[dict]:
    cmd = ["git", "log", "--pretty=format:%H|%s|%b|||"]
    if since:
        cmd.extend([f"{since}..HEAD"])
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = []
    for entry in result.stdout.split("|||"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split("|", 2)
        if len(parts) < 2:
            continue
        sha, subject = parts[0], parts[1]
        body = parts[2] if len(parts) > 2 else ""
        commits.append({"sha": sha[:7], "subject": subject, "body": body})
    return commits


def parse_commit(commit: dict) -> tuple[str, str, bool]:
    m = COMMIT_RE.match(commit["subject"])
    if not m:
        return "chore", commit["subject"], False
    breaking = bool(m.group("breaking")) or "BREAKING CHANGE:" in commit["body"]
    return m.group("type"), m.group("msg"), breaking


@click.command()
@click.option("--since", default=None, help="Tag, hash, or date to start from")
@click.option("--output", default=None, help="Write output to file instead of stdout")
def main(since: str | None, output: str | None):
    """Generate a grouped changelog from git history."""
    commits = get_commits(since)
    grouped: dict[str, list[str]] = defaultdict(list)
    breaking: list[str] = []

    for c in commits:
        ctype, msg, is_breaking = parse_commit(c)
        entry = f"- {msg} ({c['sha']})"
        grouped[ctype].append(entry)
        if is_breaking:
            breaking.append(entry)

    lines = [f"## [Unreleased] — {datetime.today().strftime('%Y-%m-%d')}\n"]

    if breaking:
        lines.append("### Breaking Changes")
        lines.extend(breaking)
        lines.append("")

    for key, label in TYPES.items():
        if grouped[key]:
            lines.append(f"### {label}")
            lines.extend(grouped[key])
            lines.append("")

    result = "\n".join(lines)

    if output:
        with open(output, "w") as f:
            f.write(result)
        console.print(f"[green]Wrote changelog to {output}[/green]")
    else:
        console.print(result)


if __name__ == "__main__":
    main()
