#!/usr/bin/env bash
# Installs Best Video Edit & Motion Collection for Claude Code and/or Codex on this computer.
# Usage: bash install.sh [claude|codex|both] [all|recommended|id1,id2,...]
# Without the second argument it shows the parts and asks. Parts already installed are kept.
# The list is in COMPONENTS.md. Needs Python 3 to read components.json.
set -euo pipefail

NAME="best-video-edit-motion-collection"
TARGET="${1:-both}"
PICK="${2:-}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$HERE/skills/$NAME"
PY=""
for CANDIDATE in python3 python; do
  if "$CANDIDATE" -c "import json" >/dev/null 2>&1; then PY="$CANDIDATE"; break; fi
done

[ -f "$SOURCE/SKILL.md" ] || { echo "Skill files not found in $SOURCE" >&2; exit 1; }
[ -n "$PY" ] || { echo "Python 3 is needed to read components.json" >&2; exit 1; }

case "$TARGET" in
  claude) ROOTS=("$HOME/.claude/skills") ;;
  codex)  ROOTS=("$HOME/.agents/skills") ;;
  both)   ROOTS=("$HOME/.claude/skills" "$HOME/.agents/skills") ;;
  *) echo "Usage: bash install.sh [claude|codex|both] [all|recommended|id1,id2,...]" >&2; exit 1 ;;
esac

manifest() { "$PY" -I -c "$1" "$SOURCE/components.json" "${@:2}"; }

if [ -z "$PICK" ]; then
  echo "Parts you can install (details in COMPONENTS.md):"
  manifest 'import json,sys
for c in json.load(open(sys.argv[1],encoding="utf-8"))["components"]:
    w="  !! "+c["warning"] if c.get("warning") else ""
    print(" %s %-18s %-12s %s%s" % ("*" if c["recommended"] else " ", c["id"], c["group"], c["size"], w))'
  echo "(* = recommended)"
  if [ -t 0 ]; then read -r -p "Type all, recommended, or part IDs separated by commas [recommended]: " PICK || true; fi
  PICK="${PICK:-recommended}"
fi

LIST_PARTS='import json,os,sys
m=json.load(open(sys.argv[1],encoding="utf-8")); pick=sys.argv[2].strip().lower(); old=sys.argv[3]
ids=[c["id"] for c in m["components"]]
if pick=="all": chosen=list(ids)
elif pick=="recommended": chosen=[c["id"] for c in m["components"] if c["recommended"]]
else:
    chosen=[p.strip() for p in pick.split(",") if p.strip()]
    bad=[p for p in chosen if p not in ids]
    if bad: sys.exit("Unknown part(s): %s. Known: %s" % (", ".join(bad), ", ".join(ids)))
if old: chosen+=[c["id"] for c in m["components"] if c["id"] not in chosen and os.path.exists(os.path.join(old,c["paths"][0]))]
print("#"+", ".join(chosen))
for p in m["core"]: print(p)
for c in m["components"]:
    if c["id"] in chosen: print("\n".join(c["paths"]))'

# Check the choice before touching any existing copy.
manifest "$LIST_PARTS" "$PICK" "" >/dev/null

for ROOT in "${ROOTS[@]}"; do
  mkdir -p "$ROOT"
  DEST="$ROOT/$NAME"
  OLD=""
  if [ -e "$DEST" ]; then
    BACKUP="$ROOT/.$NAME.backup-$(date +%Y%m%d-%H%M%S)"
    mv "$DEST" "$BACKUP"
    OLD="$BACKUP"
    echo "Previous version kept at: $BACKUP"
  fi
  # Prints the chosen IDs (first line, after #), then the relative paths to copy:
  # core + chosen parts + parts the old copy already had.
  PATHS="$(manifest "$LIST_PARTS" "$PICK" "$OLD")"
  mkdir -p "$DEST"
  PARTS=""
  while IFS= read -r REL; do
    REL="${REL%$'\r'}"
    case "$REL" in
      "#"*) PARTS="${REL#\#}" ;;
      "") ;;
      *) if [ -e "$SOURCE/$REL" ]; then mkdir -p "$(dirname "$DEST/$REL")"; cp -R "$SOURCE/$REL" "$DEST/$REL"; fi ;;
    esac
  done <<< "$PATHS"
  echo "Installed: $DEST"
  echo "Parts: core, $PARTS"
done
echo "Done. Start a new session to use the skill. Run this again with other part IDs to add parts later."
