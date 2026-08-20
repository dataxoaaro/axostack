#!/usr/bin/env bash
# Install this checkout's skills so a running agent picks them up.
#
#   scripts/sync-skills.sh           copy every skill, link any that is missing
#   scripts/sync-skills.sh --check   report drift only, exit 1 if any, write nothing
#
# Skills install as copies under $AXOSTACK_SKILL_HOME (default ~/.agents/skills),
# with a symlink at $AXOSTACK_SKILL_LINKS/<name> (default ~/.claude/skills/<name>).
# Editing this checkout changes nothing until this runs. The registry picks the
# change up live, with no restart.
#
# One directory at a time, on purpose. A single `rsync --delete` over the whole
# install directory deletes every installed skill that does not come from this
# repo, and most people have some.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO/skills"
STORE="${AXOSTACK_SKILL_HOME:-$HOME/.agents/skills}"
LINKS="${AXOSTACK_SKILL_LINKS:-$HOME/.claude/skills}"

check=0
case "${1:-}" in
	--check) check=1 ;;
	"") ;;
	*) echo "usage: $(basename "$0") [--check]" >&2; exit 2 ;;
esac

[ -d "$SRC" ] || { echo "no skills directory at $SRC" >&2; exit 2; }

synced=0
drifted=0
linked=0

if [ "$check" -eq 0 ]; then
	mkdir -p "$STORE" "$LINKS"
fi

for dir in "$SRC"/*/; do
	name="$(basename "$dir")"
	dest="$STORE/$name"

	if [ "$check" -eq 1 ]; then
		if [ ! -d "$dest" ]; then
			echo "missing:  $name"
			drifted=$((drifted + 1))
		elif ! diff -rq --exclude=.DS_Store "$dir" "$dest" >/dev/null 2>&1; then
			echo "drifted:  $name"
			drifted=$((drifted + 1))
		fi
		if [ ! -e "$LINKS/$name" ]; then
			echo "unlinked: $name"
			drifted=$((drifted + 1))
		fi
		continue
	fi

	rsync -a --delete --exclude='.DS_Store' "$dir" "$dest/"
	synced=$((synced + 1))

	if [ ! -e "$LINKS/$name" ]; then
		ln -sfn "$dest" "$LINKS/$name"
		linked=$((linked + 1))
	fi
done

total="$(find "$SRC" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"

if [ "$check" -eq 1 ]; then
	if [ "$drifted" -eq 0 ]; then
		echo "$total skills, install matches the checkout"
		exit 0
	fi
	echo
	echo "$drifted of $total skills differ. Run scripts/sync-skills.sh to fix."
	exit 1
fi

echo "$synced skills synced to $STORE"
[ "$linked" -gt 0 ] && echo "$linked new symlink(s) created in $LINKS"
exit 0
