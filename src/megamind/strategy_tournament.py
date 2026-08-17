from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Sequence


BENEFIT_FIELDS = (
    "operator_impact",
    "urgency",
    "capability_gain",
    "recruiter_leverage",
    "recovery_value",
    "composition_gain",
    "dependency_unlocking",
    "success_likelihood",
    "prior_gain_preservation",
)
COST_FIELDS = ("destructive_risk", "blocker_cost")
ALL_FIELDS = BENEFIT_FIELDS + COST_FIELDS

DEFAULT_WEIGHTS = {
    "operator_impact": 1.35,
    "urgency": 1.10,
    "capability_gain": 1.45,
    "recruiter_leverage": 1.40,
    "recovery_value": 1.15,
    "composition_gain": 1.20,
    "dependency_unlocking": 1.10,
    "success_likelihood": 1.00,
    "prior_gain_preservation": 1.25,
    "destructive_risk": 1.35,
    "blocker_cost": 1.00,
}


class StrategyValidationError(ValueError):
    """Raised when a strategy cannot be ranked safely."""


@dataclass(frozen=True)
class Strategy:
    id: str
    title: str
    tier: str
    operator_impact: float
    urgency: float
    capability_gain: float
    recruiter_leverage: float
    recovery_value: float
    composition_gain: float
    dependency_unlocking: float
    success_likelihood: float
    prior_gain_preservation: float
    destructive_risk: float
    blocker_cost: float
    blocked: bool = False
    blocker: str = ""

    @classmethod
    def from_dict(cls, value: dict) -> "Strategy":
        missing = [name for name in ("id", "title", "tier", *ALL_FIELDS) if name not in value]
        if missing:
            raise StrategyValidationError(f"missing strategy fields: {', '.join(missing)}")
        tier = str(value["tier"]).upper()
        if tier not in {"P0", "P1", "P2", "P3", "P4"}:
            raise StrategyValidationError(f"invalid tier {tier!r}")
        numeric = {}
        for name in ALL_FIELDS:
            raw = value[name]
            if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(float(raw)):
                raise StrategyValidationError(f"{name} must be a finite number")
            score = float(raw)
            if not 0.0 <= score <= 10.0:
                raise StrategyValidationError(f"{name} must be between 0 and 10")
            numeric[name] = score
        return cls(
            id=str(value["id"]),
            title=str(value["title"]),
            tier=tier,
            blocked=bool(value.get("blocked", False)),
            blocker=str(value.get("blocker", "")),
            **numeric,
        )


@dataclass(frozen=True)
class RankedStrategy:
    rank: int
    strategy_id: str
    title: str
    tier: str
    score: float
    confidence_adjusted_score: float
    pareto_front: bool
    dominated_by: tuple[str, ...]
    decision_reasons: tuple[str, ...]


class StrategyTournament:
    """Deterministic multi-objective strategy selection.

    The tournament combines three mechanisms instead of trusting a single scalar:
    1. priority-tier precedence,
    2. Pareto dominance over capability benefits and execution costs,
    3. confidence-adjusted weighted utility for deterministic tie-breaking.

    Blocked candidates remain visible in the result but can never win.
    """

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = dict(DEFAULT_WEIGHTS)
        if weights:
            unknown = set(weights) - set(ALL_FIELDS)
            if unknown:
                raise StrategyValidationError(f"unknown weight fields: {sorted(unknown)}")
            self.weights.update({key: float(value) for key, value in weights.items()})

    def _utility(self, strategy: Strategy) -> float:
        benefit = sum(getattr(strategy, field) * self.weights[field] for field in BENEFIT_FIELDS)
        cost = sum(getattr(strategy, field) * self.weights[field] for field in COST_FIELDS)
        return benefit - cost

    @staticmethod
    def _dominates(left: Strategy, right: Strategy) -> bool:
        benefits_not_worse = all(getattr(left, field) >= getattr(right, field) for field in BENEFIT_FIELDS)
        costs_not_worse = all(getattr(left, field) <= getattr(right, field) for field in COST_FIELDS)
        strictly_better = any(getattr(left, field) > getattr(right, field) for field in BENEFIT_FIELDS) or any(
            getattr(left, field) < getattr(right, field) for field in COST_FIELDS
        )
        return benefits_not_worse and costs_not_worse and strictly_better

    @staticmethod
    def _tier_rank(tier: str) -> int:
        return int(tier[1])

    def rank(self, strategies: Iterable[Strategy]) -> list[RankedStrategy]:
        candidates = list(strategies)
        if not candidates:
            raise StrategyValidationError("at least one strategy is required")
        ids = [item.id for item in candidates]
        if len(set(ids)) != len(ids):
            raise StrategyValidationError("strategy ids must be unique")

        unblocked = [item for item in candidates if not item.blocked]
        if not unblocked:
            raise StrategyValidationError("all strategies are blocked")

        best_tier = min(self._tier_rank(item.tier) for item in unblocked)
        active_tier = [item for item in unblocked if self._tier_rank(item.tier) == best_tier]

        dominated_by: dict[str, tuple[str, ...]] = {}
        for candidate in candidates:
            dominators = tuple(sorted(other.id for other in active_tier if other.id != candidate.id and self._dominates(other, candidate)))
            dominated_by[candidate.id] = dominators

        rows: list[tuple[Strategy, float, float, bool, tuple[str, ...]]] = []
        for candidate in candidates:
            raw = self._utility(candidate)
            confidence = 0.55 + (candidate.success_likelihood / 10.0) * 0.45
            adjusted = raw * confidence
            on_front = (
                not candidate.blocked
                and self._tier_rank(candidate.tier) == best_tier
                and not dominated_by[candidate.id]
            )
            rows.append((candidate, raw, adjusted, on_front, dominated_by[candidate.id]))

        rows.sort(
            key=lambda row: (
                row[0].blocked,
                self._tier_rank(row[0].tier),
                not row[3],
                -row[2],
                row[0].destructive_risk,
                row[0].blocker_cost,
                row[0].id,
            )
        )

        ranked: list[RankedStrategy] = []
        for index, (strategy, raw, adjusted, on_front, dominators) in enumerate(rows, 1):
            reasons: list[str] = []
            if strategy.blocked:
                reasons.append(f"blocked: {strategy.blocker or 'unspecified blocker'}")
            elif self._tier_rank(strategy.tier) > best_tier:
                reasons.append(f"deferred behind executable P{best_tier} work")
            elif on_front:
                reasons.append("non-dominated on active priority tier")
            else:
                reasons.append(f"dominated by {', '.join(dominators)}")
            top_benefits = sorted(
                BENEFIT_FIELDS,
                key=lambda field: getattr(strategy, field) * self.weights[field],
                reverse=True,
            )[:3]
            reasons.append("strongest benefits: " + ", ".join(top_benefits))
            reasons.append(
                f"execution costs: destructive_risk={strategy.destructive_risk:g}, blocker_cost={strategy.blocker_cost:g}"
            )
            ranked.append(
                RankedStrategy(
                    rank=index,
                    strategy_id=strategy.id,
                    title=strategy.title,
                    tier=strategy.tier,
                    score=round(raw, 4),
                    confidence_adjusted_score=round(adjusted, 4),
                    pareto_front=on_front,
                    dominated_by=dominators,
                    decision_reasons=tuple(reasons),
                )
            )
        return ranked

    def choose(self, strategies: Iterable[Strategy]) -> RankedStrategy:
        ranked = self.rank(strategies)
        return next(row for row in ranked if not row.decision_reasons[0].startswith("blocked:"))


def evaluate_payload(payload: dict) -> dict:
    raw = payload.get("strategies")
    if not isinstance(raw, list):
        raise StrategyValidationError("payload.strategies must be a list")
    strategies = [Strategy.from_dict(item) for item in raw]
    tournament = StrategyTournament(payload.get("weights"))
    ranked = tournament.rank(strategies)
    winner = next(row for row in ranked if not row.decision_reasons[0].startswith("blocked:"))
    return {
        "schema": "glaciereq.megamind.strategy-tournament.v1",
        "winner": asdict(winner),
        "ranking": [asdict(row) for row in ranked],
        "mechanisms": ["priority_tier", "pareto_dominance", "confidence_adjusted_utility"],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rank executable restoration strategies deterministically")
    parser.add_argument("input", type=Path, help="JSON file containing a strategies array")
    parser.add_argument("--output", type=Path, help="Optional output JSON path")
    args = parser.parse_args(argv)
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = evaluate_payload(payload)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
