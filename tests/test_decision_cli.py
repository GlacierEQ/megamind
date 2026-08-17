import json

from megamind.decision_cli import main


def test_decision_cli_writes_receipt(tmp_path):
    payload = {
        "candidates": [
            {
                "id": "wanted",
                "title": "Wanted",
                "tier": "P1",
                "operator_impact": 9,
                "urgency": 8,
                "capability_gain": 9,
                "recruiter_leverage": 10,
                "recovery_value": 8,
                "composition_gain": 9,
                "dependency_unlocking": 8,
                "success_likelihood": 9,
                "prior_gain_preservation": 9,
                "destructive_risk": 1,
                "blocker_cost": 1,
                "market_demand": 10,
                "differentiation": 10,
                "evidence_strength": 9,
                "strategic_fit": 10,
                "time_to_value": 9,
                "reversibility": 9,
                "estimated_effort": 1
            }
        ],
        "effort_budget": 2
    }
    source = tmp_path / "candidates.json"
    output = tmp_path / "receipt.json"
    source.write_text(json.dumps(payload), encoding="utf-8")

    assert main([str(source), "--output", str(output)]) == 0
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["schema"] == "glaciereq.megamind.decision-intelligence.v2"
    assert receipt["winner"]["candidate_id"] == "wanted"
    assert receipt["plan"]["selected_ids"] == ["wanted"]
