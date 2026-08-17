import pytest

from megamind.decision_intelligence import (
    DecisionCandidate,
    DecisionIntelligenceEngine,
    evaluate_decision_payload,
)
from megamind.strategy_tournament import StrategyValidationError


def candidate(id_, tier="P1", **overrides):
    base = {
        "id": id_,
        "title": id_.replace("_", " ").title(),
        "tier": tier,
        "operator_impact": 8,
        "urgency": 7,
        "capability_gain": 8,
        "recruiter_leverage": 8,
        "recovery_value": 7,
        "composition_gain": 7,
        "dependency_unlocking": 6,
        "success_likelihood": 8,
        "prior_gain_preservation": 9,
        "destructive_risk": 2,
        "blocker_cost": 2,
        "market_demand": 8,
        "differentiation": 8,
        "evidence_strength": 8,
        "strategic_fit": 8,
        "time_to_value": 7,
        "reversibility": 8,
        "estimated_effort": 2,
    }
    base.update(overrides)
    return DecisionCandidate.from_dict(base)


def test_recruiter_demand_can_break_same_tier_tie():
    engine = DecisionIntelligenceEngine()
    commodity = candidate("commodity", market_demand=5, differentiation=3, recruiter_leverage=6)
    wanted = candidate("wanted", market_demand=10, differentiation=10, recruiter_leverage=10)
    assert engine.choose([commodity, wanted]).candidate_id == "wanted"


def test_p0_still_beats_shiny_p1():
    engine = DecisionIntelligenceEngine()
    urgent = candidate("urgent", tier="P0", market_demand=2, differentiation=2)
    shiny = candidate("shiny", tier="P1", market_demand=10, differentiation=10)
    assert engine.choose([shiny, urgent]).candidate_id == "urgent"


def test_low_regret_balanced_candidate_beats_fragile_spike():
    engine = DecisionIntelligenceEngine()
    balanced = candidate("balanced")
    spike = candidate(
        "spike",
        recruiter_leverage=10,
        market_demand=10,
        differentiation=10,
        recovery_value=1,
        prior_gain_preservation=2,
        reversibility=2,
        destructive_risk=8,
    )
    assert engine.choose([spike, balanced]).candidate_id == "balanced"


def test_unsatisfied_dependency_cannot_win():
    engine = DecisionIntelligenceEngine()
    dependent = candidate("dependent", dependencies=["foundation"], market_demand=10)
    foundation = candidate("foundation", tier="P2")
    winner = engine.choose([dependent, foundation])
    assert winner.candidate_id == "foundation"


def test_dependency_becomes_eligible_after_completion():
    engine = DecisionIntelligenceEngine()
    dependent = candidate("dependent", dependencies=["foundation"], market_demand=10)
    foundation = candidate("foundation", tier="P2")
    winner = engine.choose([dependent, foundation], completed=["foundation"])
    assert winner.candidate_id == "dependent"


def test_budgeted_plan_unlocks_dependency_chain():
    engine = DecisionIntelligenceEngine()
    foundation = candidate("foundation", estimated_effort=2, dependency_unlocking=10)
    amplifier = candidate("amplifier", estimated_effort=2, dependencies=["foundation"], capability_gain=10)
    distraction = candidate("distraction", tier="P2", estimated_effort=2, market_demand=10)
    plan = engine.build_plan([amplifier, distraction, foundation], effort_budget=4)
    assert plan["selected_ids"] == ["foundation", "amplifier"]
    assert plan["effort_spent"] == 4


def test_conflicting_candidate_is_not_selected_into_same_plan():
    engine = DecisionIntelligenceEngine()
    alpha = candidate("alpha", estimated_effort=1, conflicts=["beta"], market_demand=10)
    beta = candidate("beta", estimated_effort=1, conflicts=["alpha"], market_demand=9)
    plan = engine.build_plan([alpha, beta], effort_budget=2)
    assert len(plan["selected_ids"]) == 1


def test_payload_exposes_intelligence_mechanisms_and_plan():
    payload = {
        "candidates": [
            {
                **{
                    "id": "winner",
                    "title": "Winner",
                    "tier": "P1",
                    "operator_impact": 9,
                    "urgency": 9,
                    "capability_gain": 9,
                    "recruiter_leverage": 10,
                    "recovery_value": 8,
                    "composition_gain": 9,
                    "dependency_unlocking": 8,
                    "success_likelihood": 9,
                    "prior_gain_preservation": 9,
                    "destructive_risk": 1,
                    "blocker_cost": 1,
                },
                "market_demand": 10,
                "differentiation": 10,
                "evidence_strength": 9,
                "strategic_fit": 10,
                "time_to_value": 9,
                "reversibility": 9,
                "estimated_effort": 1,
            }
        ],
        "effort_budget": 2,
    }
    result = evaluate_decision_payload(payload)
    assert result["winner"]["candidate_id"] == "winner"
    assert "minimax_regret" in result["mechanisms"]
    assert "pairwise_outranking" in result["mechanisms"]
    assert result["plan"]["selected_ids"] == ["winner"]


def test_unknown_dependency_fails_closed():
    engine = DecisionIntelligenceEngine()
    broken = candidate("broken", dependencies=["missing"])
    with pytest.raises(StrategyValidationError, match="unknown dependencies"):
        engine.rank([broken])
