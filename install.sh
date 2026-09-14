#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:---global}"

case "$MODE" in
  --global)
    TARGET="$HOME/.claude/skills"
    ;;
  --project)
    TARGET="$PWD/.claude/skills"
    ;;
  --uninstall)
    for skill in "$ROOT"/skills/*; do
      name="$(basename "$skill")"
      path="$HOME/.claude/skills/$name"
      if [[ -L "$path" && "$(readlink "$path")" == "$skill" ]]; then
        rm "$path"
        echo "Removed $name"
      fi
    done
    exit 0
    ;;
  *)
    echo "Usage: ./install.sh [--global | --project | --uninstall]"
    exit 2
    ;;
esac

mkdir -p "$TARGET"

for skill in "$ROOT"/skills/*; do
  [[ -d "$skill" && -f "$skill/SKILL.md" ]] || continue
  name="$(basename "$skill")"
  destination="$TARGET/$name"

  if [[ -L "$destination" ]]; then
    rm "$destination"
  elif [[ -e "$destination" ]]; then
    echo "Refusing to replace existing $destination"
    echo "Move it away, then run the installer again."
    exit 1
  fi

  ln -s "$skill" "$destination"
  echo "Installed /$name"
done

mkdir -p "$HOME/.linkedin-content/inbox"
mkdir -p "$HOME/.linkedin-content/drafts"
mkdir -p "$HOME/.linkedin-content/posted"

PROFILE="$HOME/.linkedin-content/profile.md"
if [[ ! -e "$PROFILE" ]]; then
  cp "$ROOT/references/voice-supreet.md" "$PROFILE"
  printf '\n## Notes supplied by Supreet\n\nAdd dated, verbatim notes below this line.\n' >> "$PROFILE"
  echo "Created private profile at $PROFILE"
else
  echo "Kept existing private profile at $PROFILE"
fi

SLACK="$HOME/.linkedin-content/slack.md"
if [[ ! -e "$SLACK" ]]; then
  cp "$ROOT/references/slack-channels.md" "$SLACK"
  echo "Created Slack channel config at $SLACK"
else
  echo "Kept existing Slack channel config at $SLACK"
fi

echo
echo "Ready. Start Claude Code and run: /linkedin-today"
