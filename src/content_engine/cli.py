from __future__ import annotations

import argparse
import json
import logging
import sys

from .config import Config
from .engine import ContentEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the LinkedIn content engine")
    parser.add_argument(
        "command", nargs="?", default="run", choices=["run", "check-config"]
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    try:
        config = Config.from_env()
        config.validate_publish()
        if args.command == "check-config":
            print(
                json.dumps(
                    {
                        "repository": config.github_repository,
                        "channel": config.slack_channel_id,
                        "approver": config.slack_approver_user_id,
                        "model": config.anthropic_model,
                        "publishing": config.publish_enabled,
                    },
                    indent=2,
                )
            )
            return 0
        counts = ContentEngine(config).run()
        print(json.dumps(counts, indent=2))
        return 0
    except Exception:
        logging.exception("Content engine failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
