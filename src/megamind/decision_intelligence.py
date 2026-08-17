from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Iterable

from .strategy_tournament import Strategy, StrategyValidationError


SCENARIOS = {
    "recruiter_demand": {
        "operator_impact": 1.1,
        "capability_gain": 1.2,
        "recruiter_leverage": 1.8,
        "market_demand": 1.8,
        "differentiation": 1.5,
        "evidence_strength": 1.3,
        "strategic_fit": 1.2,
        "time_to_value": 1.0,
        "destructive_risk": -1.2,
        "blocker_cost": -0.8,
    },
    "capability_compounding": {
        "operator_impact": 1.2,
        "capability_gain": 1.8,
        "composition_gain": 1.6,
        "dependency_unlocking": 1.5,
        "differentiation": 1.2,
        "evidence_strength": 1.0,
        "strategic_fit": 1.3,
        "reversibility": 0.8,
        "destructive_risk": -1.3,
        "blocker_cost": -0.8,
    },
    "recovery_resilience": {
        "operator_impact": 1.3,
        "recovery_value": 1.8,
        "prior_gain_preservation": 1.7,
        "success_likelihood": 1.4,
        "evidence_strength": 1.3,
        "reversibility": 1.2,
        "time_to_value": 0.8,
        "destructive_risk": -1.8,
        "blocker_cost": -1.2,
    },
}


@dataclass(frozen=True)
class DecisionCandidate:
    strategy: Strategy
    market_demand: float = 5.0
    differentiation: float = 5.0
    evidence_strength: float = 5.0
    strategic_fit: float = 5.0
    time_to_value: float = 5.0
    reversibility: float = 5.0
    estimated_effort: float = 1.0
    dependencies: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, value: dict) -> "DecisionCandidate":
        strategy = Strategy.from_dict(value)
        extras = {}
        for field in (
            "market_demand",
            "differentiation",
            "evidence_strength",
            "strategic_fit",
            "time_to_value",
            "reversibility",
        ):
            raw = value.get(field, 5.0)
            if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                raise StrategyValidationError(f"{field} must be numeric")
            score = float(raw)
            if not 0.0 <= score <= 10.0:
                raise StrategyValidationError(f"{field} must be between 0 and 10")
            extras[field] = score
        effort = float(value.get("estimated_effort", 1.0))
        if not 0.0 < effort <= 100.0:
            raise StrategyValidationError("estimated_effort must be > 0 and <= 100")
        dependencies = tuple(str(item) for item in value.get("dependencies", ()))
        conflicts = tuple(str(item) for item in value.get("conflicts", ()))
        if strategy.id in dependencies or strategy.id in conflicts:
            raise StrategyValidationError("candidate cannot depend on or conflict with itself")
        return cls(
            strategy=strategy,
            estimated_effort=effort,
            dependencies=dependencies,
            conflicts=conflicts,
            **extras,
        )

    def metric(self, name: str) -> float:
        if hasattr(self.strategy, name):
            return float(getattr(self.strategy, name))
        return float(getattr(self, name))


@dataclass(frozen=True)
class IntelligentDecision:
    rank: int
    candidate_id: str
    title: str
    tier: str
    robust_score: float
    mean_utility: float
    worst_case_regret: float
    outranking_wins: int
    scenario_scores: dict[str, float]
    dependencies_satisfied: bool
    reasons: tuple[str, ...]


class DecisionIntelligenceEngine:
    """Robust decision layer for high-value engineering choices.

    It combines priority precedence, scenario analysis, minimax regret, pairwise
    outranking, dependency feasibility, and portfolio-level budget allocation.
    The result is intentionally harder to game than a single weighted score.
    """

    def __init__(self, *, regret_penalty: float = 0.35, outranking_bonus: float = 0.20) -> None:
        self.regret_penalty = regret_penalty
        self.outranking_bonus = outranking_bonus

    @staticmethod
    def _tier_rank(tier: str) -> int:
        return int(tier[1])

    @staticmethod
    def _scenario_score(candidate: DecisionCandidate, weights: dict[str, float]) -> float:
        return sum(candidate.metric(field) * weight for field, weight in weights.items())

    def rank(
        self,
        candidates: Iterable[DecisionCandidate],
        *,
        completed: Iterable[str] = (),
    ) -> list[IntelligentDecision]:
        rows = list(candidates)
        if not rows:
            raise StrategyValidationError("at least one decision candidate is required")
        ids = [row.strategy.id for row in rows]
        if len(ids) != len(set(ids)):
            raise StrategyValidationError("candidate ids must be unique")
        known = set(ids) | set(completed)
        for row in rows:
            unknown = set(row.dependencies) - known
            if unknown:
                raise StrategyValidationError(
                    f"{row.strategy.id} has unknown dependencies: {sorted(unknown)}"
                )

        completed_set = set(completed)
        feasible = [
            row
            for row in rows
            if not row.strategy.blocked and set(row.dependencies).issubset(completed_set)
        ]
        if not feasible:
            raise StrategyValidationError("no unblocked candidate has satisfied dependencies")
        best_tier = min(self._tier_rank(row.strategy.tier) for row in feasible)
        active = [row for row in feasible if self._tier_rank(row.strategy.tier) == best_tier]

        scenario_scores = {
            row.strategy.id: {
                name: self._scenario_score(row, weights) for name, weights in SCENARIOS.items()
            }
            for row in active
        }
        best_by_scenario = {
            name: max(scores[name] for scores in scenario_scores.values()) for name in SCENARIOS
        }

        decisions: list[IntelligentDecision] = []
        for row in rows:
            sid = row.strategy.id
            deps_ok = set(row.dependencies).issubset(completed_set)
            if row in active:
                scores = scenario_scores[sid]
                regrets = [best_by_scenario[name] - scores[name] for name in SCENARIOS]
                worst_regret = max(regrets)
                wins = 0
                for other in active:
                    if other.strategy.id == sid:
                        continue
                    left = scenario_scores[sid]
                    right = scenario_scores[other.strategy.id]
                    if sum(left[name] > right[name] for name in SCENARIOS) >= 2:
                        wins += 1
                avg = mean(scores.values())
                robust = avg - self.regret_penalty * worst_regret + self.outranking_bonus * wins
                reasons = (
                    "active highest-priority executable tier",
                    f"worst-case regret={worst_regret:.3f}",
                    f"pairwise outranking wins={wins}",
                    "scenario-balanced across recruiter demand, capability compounding, and recovery resilience",
                )
            else:
                scores = {name: self._scenario_score(row, weights) for name, weights in SCENARIOS.items()}
                avg = mean(scores.values())
                worst_regret = 0.0
                wins = 0
                robust = avg - 10_000.0
                reason = "blocked" if row.strategy.blocked else (
                    "dependencies unsatisfied" if not deps_ok else f"deferred behind P{best_tier}"
                )
                reasons = (reason,)
            decisions.append(
                IntelligentDecision(
                    rank=0,
                    candidate_id=sid,
                    title=row.strategy.title,
                    tier=row.strategy.tier,
                    robust_score=round(robust, 4),
                    mean_utility=round(avg, 4),
                    worst_case_regret=round(worst_regret, 4),
                    outranking_wins=wins,
                    scenario_scores={key: round(value, 4) for key, value in scores.items()},
                    dependencies_satisfied=deps_ok,
                    reasons=reasons,
                )
            )

        decisions.sort(key=lambda item: (-item.robust_score, item.candidate_id))
        return [IntelligentDecision(rank=i, **{k: v for k, v in asdict(item).items() if k != "rank"}) for i, item in enumerate(decisions, 1)]

    def choose(self, candidates: Iterable[DecisionCandidate], *, completed: Iterable[str] = ()) -> IntelligentDecision:
        return self.rank(candidates, completed=completed)[0]

    def build_plan(
        self,
        candidates: Iterable[DecisionCandidate],
        *,
        effort_budget: float,
        completed: Iterable[str] = (),
    ) -> dict:
        if effort_budget <= 0:
            raise StrategyValidationError("effort_budget must be positive")
        pool = list(candidates)
        selected: list[IntelligentDecision] = []
        selected_ids: set[str] = set()
        completed_set = set(completed)
        spent = 0.0

        while True:
            eligible = [
                row for row in pool
                if row.strategy.id not in selected_ids
                and not row.strategy.blocked
                and set(row.dependencies).issubset(completed_set | selected_ids)
                and row.estimated_effort + spent <= effort_budget
                and not (set(row.conflicts) & selected_ids)
            ]
            if not eligible:
                break
            ranked = self.rank(eligible, completed=completed_set | selected_ids)
            winner = ranked[0]
            candidate = next(row for row in eligible if row.strategy.id == winner.candidate_id)
            selected.append(winner)
            selected_ids.add(candidate.strategy.id)
            spent += candidate.estimated_effort

        return {
            "schema": "glaciereq.megamind.decision-intelligence.v2",
            "selected": [asdict(item) for item in selected],
            "selected_ids": [item.candidate_id for item in selected],
            "effort_budget": effort_budget,
            "effort_spent": round(spent, 4),
            "effort_remaining": round(effort_budget - spent, 4),
            "mechanisms": [
                "priority_precedence",
                "scenario_analysis",
                "minimax_regret",
                "pairwise_outranking",
                "dependency_feasibility",
                "budgeted_portfolio_selection",
            ],
        }


def evaluate_decision_payload(payload: dict) -> dict:
    raw = payload.get("candidates")
    if not isinstance(raw, list):
        raise StrategyValidationError("payload.candidates must be a list")
    candidates = [DecisionCandidate.from_dict(item) for item in raw]
    engine = DecisionIntelligenceEngine()
    completed = payload.get("completed", [])
    ranking = engine.rank(candidates, completed=completed)
    result = {
        "schema": "glaciereq.megamind.decision-intelligence.v2",
        "winner": asdict(ranking[0]),
        "ranking": [asdict(item) for item in ranking],
        "mechanisms": [
            "priority_precedence",
            "scenario_analysis",
            "minimax_regret",
            "pairwise_outranking",
            "dependency_feasibility",
        ],
    }
    if "effort_budget" in payload:
        result["plan"] = engine.build_plan(
            candidates,
            effort_budget=float(payload["effort_budget"]),
            completed=completed,
        )
    return result
