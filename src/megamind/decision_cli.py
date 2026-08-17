from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .decision_intelligence import evaluate_decision_payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rank high-value engineering and job strategies with Megamind Decision Intelligence v2"
    )
    parser.add_argument("input", type=Path, help="JSON file containing candidates")
    parser.add_argument("--output", type=Path, help="Optional JSON receipt output")
    args = parser.parse_args(argv)

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = evaluate_decision_payload(payload)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
