# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`h2h-galleryinfo-parser` is a small Python library (published to PyPI as `h2h-galleryinfo-parser`, imported as `h2h_galleryinfo_parser`) that parses `galleryinfo.txt` metadata files produced by H@H (Hentai@Home Downloader). It also includes a parser for exhentai.org / e-hentai.org gallery URLs. There is no CLI or service — this is a library only.

## Build & Development Commands

```bash
# Install package + dev tools (black, ruff, mypy, pymarkdownlnt)
uv pip install -e ".[dev]"

# Run tests
uv run python -m unittest discover -s tests -v

# Type checking (strict mode, configured in mypy.ini)
uv run mypy src tests

# Linting with ruff (rules in pyproject.toml: E, F, I, UP)
uv run ruff check .

# Formatting with black (88 char line length)
uv run black src tests
```

- Always use `uv run python` to run scripts, tests, or ad-hoc snippets, so the venv's dev tools resolve consistently with the IDE and the Stop hooks (see Code Style below).
- A Stop hook ([.claude/hooks/finalize-python.sh](.claude/hooks/finalize-python.sh)) already runs black → ruff --fix → black → mypy over `src` and `tests` after each turn, so manual formatting/type-check passes are mostly a sanity check, not the primary gate.
- If the `.venv` is corrupted (e.g. after a Python version upgrade), run [scripts/rebuild-env.sh](scripts/rebuild-env.sh) to wipe it and tool caches and reinstall from scratch.

## Architecture

Two independent parsers are exported from `__init__.py`: `galleryinfo_parser.py` (parses a downloaded gallery's `galleryinfo.txt`) and `gallery_url_parser.py` (parses exhentai.org/e-hentai.org gallery URLs). They don't interact — read each file directly for what it does.

Gotchas that aren't obvious from a quick read:

- Installed package name (`h2h_galleryinfo_parser`) differs from the source directory (`src/galleryinfo_parser/`) via the `package-dir` remap in `pyproject.toml`. Internal code/tests import via `src.galleryinfo_parser...`; external/doc examples use `h2h_galleryinfo_parser`.
- `GalleryInfoParser.tags` is `list[tuple[str, str]]`, not the `dict[str, str]` its docstring claims.
- Comment parsing in `parse_galleryinfo` ends at a hardcoded sentinel line (the H@H downloader's footer string), not at EOF or a blank line — a format change in that footer would silently break comment extraction.

## Coding Guidelines

This is a solo, pre-1.0 project with no external consumers pinned to current APIs. Do not optimize for minimal diffs or backward compatibility:

- Freely rename, restructure, or delete code when it improves the design — there are no external callers to break.
- Do not keep deprecated aliases, compatibility shims, or old code paths "just in case."
- Prefer the cleanest end state over the smallest diff to get there.

Follow SOLID principles when writing code:

- **Single Responsibility** - Each class/module should have one reason to change
- **Open/Closed** - Open for extension, closed for modification (use inheritance/composition)
- **Liskov Substitution** - Subtypes must be substitutable for their base types
- **Interface Segregation** - Prefer small, specific interfaces over large ones
- **Dependency Inversion** - Depend on abstractions (ABC), not concrete implementations

## Code Style

- **Sync obligation for tooling configuration:** the IDE save pipeline and the Stop hook pipeline are kept in lockstep across the locations below. Any change to one of them requires matching updates to the others in the same change.
  - Python formatting/lint/type-check: [.vscode/settings.json](.vscode/settings.json) (`[python]` block), the `[tool.ruff]` section of [pyproject.toml](pyproject.toml), [mypy.ini](mypy.ini), and [.claude/hooks/finalize-python.sh](.claude/hooks/finalize-python.sh).
  - Markdown formatting: [.vscode/settings.json](.vscode/settings.json) (`[markdown]` block) and [.claude/hooks/finalize-markdown.sh](.claude/hooks/finalize-markdown.sh).
  - Tool versions: the `dev` group of `[project.optional-dependencies]` in [pyproject.toml](pyproject.toml) pins `black`, `ruff`, `mypy`, and `pymarkdownlnt`. Both the IDE pipeline (when invoked via `uv run`) and the Stop hooks resolve to these venv-installed versions, so bumping any of them must be done here — not via Homebrew or any other system-wide install.
- Python version range: refer to `requires-python` in [pyproject.toml](pyproject.toml)
