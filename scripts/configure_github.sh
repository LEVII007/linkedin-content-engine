#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 OWNER/REPO SLACK_CHANNEL_ID SUPREET_SLACK_USER_ID"
  exit 2
fi

REPO="$1"
CHANNEL_ID="$2"
APPROVER_ID="$3"

read -rsp "Slack bot token: " SLACK_TOKEN
echo
read -rsp "Anthropic API key: " ANTHROPIC_KEY
echo

gh secret set SLACK_BOT_TOKEN --repo "$REPO" --body "$SLACK_TOKEN"
gh secret set ANTHROPIC_API_KEY --repo "$REPO" --body "$ANTHROPIC_KEY"
gh variable set SLACK_CHANNEL_ID --repo "$REPO" --body "$CHANNEL_ID"
gh variable set SLACK_APPROVER_USER_ID --repo "$REPO" --body "$APPROVER_ID"
gh variable set ANTHROPIC_MODEL --repo "$REPO" --body "claude-sonnet-5"
gh variable set PUBLISH_ENABLED --repo "$REPO" --body "false"

echo "Base configuration stored. Publishing remains OFF."
echo "Next: run scripts/linkedin_auth_github.py, then set PUBLISH_ENABLED=true."
