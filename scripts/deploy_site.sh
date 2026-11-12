#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE_SRC="$REPO_ROOT/docs/index.html"
REMOTE_URL="https://github.com/cedpaul13/hoops_8ultime_2026_womens.git"

if [ ! -f "$SITE_SRC" ]; then
  echo "Error: $SITE_SRC not found. Restore the versioned site source before deploying." >&2
  exit 1
fi

(cd "$REPO_ROOT" && npm test)
REMOTE_TIP="$(git ls-remote --heads "$REMOTE_URL" refs/heads/gh-pages | cut -f1)"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cp "$SITE_SRC" "$TMP_DIR/index.html"
touch "$TMP_DIR/.nojekyll"

cd "$TMP_DIR"
git init -q -b gh-pages
git add -A
git -c user.name="deploy-bot" -c user.email="deploy@local" commit -q -m "Deploy site" \
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git remote add origin "$REMOTE_URL"
git push "--force-with-lease=refs/heads/gh-pages:$REMOTE_TIP" origin HEAD:refs/heads/gh-pages

echo "Deployed docs/index.html to gh-pages on $REMOTE_URL"
echo "First-time setup only: enable Settings -> Pages -> Deploy from a branch -> gh-pages / (root)."
echo "Live URL: https://cedpaul13.github.io/hoops_8ultime_2026_womens/"
