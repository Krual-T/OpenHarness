#!/usr/bin/env bash
set -euo pipefail

OH_CLONE="$HOME/.agents/skill-hub/openharness"
OH_REPO="https://github.com/Krual-T/OpenHarness.git"

usage() {
    cat <<'EOF'
Usage: install.sh [--branch <branch>]

Install the OpenHarness CLI tool globally.

  --branch, -b   Clone or checkout a specific branch (default: default branch)
  --help, -h     Show this help

After installation, run this in each project:
  openharness init --agent <claude|codex|all>
EOF
    exit 0
}

BRANCH=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --branch|-b)
            BRANCH="$2"; shift 2 ;;
        --help|-h)
            usage ;;
        *)
            echo "Unknown option: $1"
            usage ;;
    esac
done

# Prerequisites
for cmd in git uv; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "ERROR: $cmd is required but not found"
        exit 1
    fi
done

# Clone or update
if [ -d "$OH_CLONE/.git" ]; then
    echo "Updating OpenHarness at $OH_CLONE ..."
    (cd "$OH_CLONE" && git pull)
else
    if [ -d "$OH_CLONE" ]; then
        echo "ERROR: $OH_CLONE exists but is not a git repository"
        echo "Remove it manually and retry."
        exit 1
    fi
    echo "Cloning OpenHarness to $OH_CLONE ..."
    mkdir -p "$(dirname "$OH_CLONE")"
    if [ -n "$BRANCH" ]; then
        git clone --branch "$BRANCH" "$OH_REPO" "$OH_CLONE"
    else
        git clone "$OH_REPO" "$OH_CLONE"
    fi
fi

# Checkout branch if specified and repo already exists
if [ -n "$BRANCH" ]; then
    (cd "$OH_CLONE" && git checkout "$BRANCH")
fi

# Install CLI
echo "Installing openharness CLI ..."
uv tool install --editable "$OH_CLONE"

# Install shell completion
echo ""
echo "Installing shell completion..."
case "${SHELL##*/}" in
    bash)
        openharness --show-completion >> "$HOME/.bashrc"
        echo "  Completion installed to ~/.bashrc (生效需新开终端或 source ~/.bashrc)"
        ;;
    zsh|fish)
        echo "  Run 'openharness --install-completion' to install completion for ${SHELL##*/}"
        ;;
    *)
        echo "  Unknown shell: run 'openharness --install-completion' to install completion manually"
        ;;
esac

echo ""
echo "OpenHarness installed. Next, run this in each project:"
echo "  openharness init --agent <claude|codex|all>"
