# GitDigest

> CLI that reads your git log and generates a clean, grouped changelog in seconds

## What it does
Parses `git log` output from any repo, groups commits by type (feat / fix / refactor / docs / chore), and writes a formatted `CHANGELOG.md`. Follows Conventional Commits spec. Works on any git repo — no setup files needed.

## Quick Start
```bash
git clone https://github.com/MrHassan2027/GitDigest
cd GitDigest
pip install -e .

gitdigest                        # changelog for current repo
gitdigest --since v1.0.0         # since a tag
gitdigest --output CHANGELOG.md  # write to file
```

## Features
- Groups commits: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`
- Detects breaking changes (`!` suffix or `BREAKING CHANGE:` footer)
- `--since <tag|date|hash>` range filter
- Outputs Markdown or plain text
- Works offline — only reads local git history

## Tech Stack
| Tool | Why |
|------|-----|
| Python 3.11+ | `subprocess` to call git, `re` for parsing |
| `click` | CLI argument handling |
| `rich` | Colored terminal output |

## Example Output
```markdown
## [Unreleased]

### Features
- add user authentication flow (#42)
- support dark mode in dashboard

### Bug Fixes
- fix crash on empty config file
- correct timezone offset in reports

### Breaking Changes
- remove legacy v1 API endpoints
```
