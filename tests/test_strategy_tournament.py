import json

import pytest

from megamind.strategy_tournament import Strategy, StrategyTournament, StrategyValidationError, evaluate_payload


def strategy(strategy_id: str, tier: str = "P1", **overrides):
    base = {
        "id": strategy_id,
        "title": strategy_id.replace("-", " ").title(),
        "tier": tier,
        "operator_impact": 7,
        "urgency": 7,
        "capability_gain": 7,
        "recruiter_leverage": 7,
        "recovery_value": 7,
        "composition_gain": 7,
        "dependency_unlocking": 7,
        "success_likelihood": 7,
        "prior_gain_preservation": 8,
        "destructive_risk": 2,
        "blocker_cost": 2,
    }
    base.update(overrides)
    return Strategy.from_dict(base)


def test_p0_preempts_higher_utility_p1():
    tournament = StrategyTournament()
    winner = tournament.choose([
        strategy("p1-monster", "P1", capability_gain=10, recruiter_leverage=10),
        strategy("p0-repair", "P0", capability_gain=5, recruiter_leverage=5),
    ])
    assert winner.strategy_id == "p0-repair"


def test_blocked_candidate_cannot_win():
    tournament = StrategyTournament()
    winner = tournament.choose([
        strategy("blocked", "P0", capability_gain=10, blocked=True, blocker="provider unavailable"),
        strategy("executable", "P1", capability_gain=6),
    ])
    assert winner.strategy_id == "executable"


def test_pareto_dominance_precedes_scalar_tie_break():
    tournament = StrategyTournament()
    dominant = strategy(
        "dominant",
        capability_gain=9,
        recruiter_leverage=9,
        destructive_risk=1,
        blocker_cost=1,
    )
    dominated = strategy(
        "dominated",
        capability_gain=8,
        recruiter_leverage=8,
        destructive_risk=2,
        blocker_cost=2,
    )
    ranked = tournament.rank([dominated, dominant])
    assert ranked[0].strategy_id == "dominant"
    assert ranked[0].pareto_front is True
    loser = next(row for row in ranked if row.strategy_id == "dominated")
    assert loser.dominated_by == ("dominant",)


def test_confidence_penalizes_speculative_strategy():
    tournament = StrategyTournament()
    steady = strategy("steady", success_likelihood=9, capability_gain=8)
    speculative = strategy("speculative", success_likelihood=2, capability_gain=9)
    ranked = tournament.rank([steady, speculative])
    assert ranked[0].strategy_id == "steady"


def test_payload_emits_machine_readable_three_mechanism_receipt():
    result = evaluate_payload({"strategies": [strategy("one").__dict__, strategy("two", capability_gain=8).__dict__]})
    assert result["schema"] == "glaciereq.megamind.strategy-tournament.v1"
    assert result["mechanisms"] == [
        "priority_tier",
        "pareto_dominance",
        "confidence_adjusted_utility",
    ]
    json.dumps(result)


def test_rejects_out_of_range_scores():
    with pytest.raises(StrategyValidationError, match="between 0 and 10"):
        strategy("bad", capability_gain=11)


def test_rejects_duplicate_ids():
    tournament = StrategyTournament()
    with pytest.raises(StrategyValidationError, match="unique"):
        tournament.rank([strategy("same"), strategy("same")])


def test_rejects_all_blocked_queue():
    tournament = StrategyTournament()
    with pytest.raises(StrategyValidationError, match="all strategies are blocked"):
        tournament.rank([strategy("dead", blocked=True)])
