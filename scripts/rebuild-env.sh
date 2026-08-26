#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repository_root"

command -v uv >/dev/null || {
    printf 'rebuild-env: uv is required\n' >&2
    exit 1
}
command -v npm >/dev/null || {
    printf 'rebuild-env: npm is required\n' >&2
    exit 1
}

# These commands resolve from pyproject.toml and package.json, not lockfiles.
uv venv --clear --python 3.14 .venv
uv pip install --python .venv/bin/python --upgrade --reinstall -e '.[dev]'
npm install --package-lock=false
