import pytest
from megamind import SecretAlphaMasterEngine

def test_secret_alpha_master_engine():
    engine = SecretAlphaMasterEngine()
    revealed = engine.get_revealed_aliases()
    assert len(revealed) == 14
    aliases = [r["public_alias"] for r in revealed]
    assert "Quasar Alpha" in aliases
    assert "Spectre" in aliases
    assert "Pony Alpha" in aliases

    cloaked = engine.get_cloaked_releases()
    assert len(cloaked) == 7

    targets = engine.get_preservation_targets()
    assert len(targets) == 6

    lineages = engine.get_internal_stealth_lineages()
    assert len(lineages) == 14

    summary = engine.get_master_audit_summary()
    assert summary["total_external_master_records"] == 27
    assert summary["total_internal_stealth_lineages"] == 14
