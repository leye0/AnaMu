"""Check source capabilities and the truthfulness of proposed research claims.

Usage:
  python -m scripts.validate_research_contracts
  python -m scripts.validate_research_contracts --proposal /tmp/proposal.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from anamu.research_contracts import (ResearchContractError, check_experiment,
                                      load_catalog, validate_catalog)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", type=Path,
                        help="JSON with one new experiment using the same contract fields")
    args = parser.parse_args()
    try:
        catalog = load_catalog()
        validate_catalog(catalog)
        if args.proposal:
            check_experiment(args.proposal.stem,
                             json.loads(args.proposal.read_text(encoding="utf-8")), catalog)
    except (ResearchContractError, ValueError, KeyError) as error:
        parser.exit(1, f"research evidence rejected: {error}\n")
    print(f"OK: {len(catalog['sources'])} sources, "
          f"{len(catalog['methods'])} methods, "
          f"{len(catalog['experiments'])} registered experiments")
    if args.proposal:
        print(f"OK: compatible proposal {args.proposal}")


if __name__ == "__main__":
    main()
