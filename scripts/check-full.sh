#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repository_root"

scripts/check-fast.sh
.venv/bin/pytest

rm -rf build dist
.venv/bin/python -m build --no-isolation

smoke_root="$(mktemp -d "${TMPDIR:-/tmp}/gallery-wheel-smoke.XXXXXX")"
trap 'rm -rf "$smoke_root"' EXIT
.venv/bin/python -m venv "$smoke_root/venv"
wheel="$(find dist -maxdepth 1 -name '*.whl' -print -quit)"
[[ -n "$wheel" ]] || {
    printf 'check-full: built wheel was not found\n' >&2
    exit 1
}
"$smoke_root/venv/bin/python" -m pip install --no-deps "$wheel"
"$smoke_root/venv/bin/python" -c 'import h2h_galleryinfo_parser'
