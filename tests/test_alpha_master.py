from megamind import SecretAlphaMasterEngine


def test_secret_alpha_master_engine() -> None:
    engine = SecretAlphaMasterEngine()
    revealed = engine.get_revealed_aliases()
    assert len(revealed) == 14
    aliases = [record["public_alias"] for record in revealed]
    assert "Quasar Alpha" in aliases
    assert "Spectre" in aliases
    assert "Pony Alpha" in aliases

    cloaked = engine.get_cloaked_releases()
    assert len(cloaked) == 7

    targets = engine.get_preservation_targets()
    assert len(targets) == 6

    lineages = engine.get_internal_stealth_lineages()
    assert len(lineages) == 15

    summary = engine.get_master_audit_summary()
    assert summary["total_external_master_records"] == (
        len(revealed) + len(cloaked) + len(targets)
    )
    assert summary["total_internal_stealth_lineages"] == len(lineages)
