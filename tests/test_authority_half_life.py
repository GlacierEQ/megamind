from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "authority_half_life",
    _ROOT / "src" / "megamind" / "authority_half_life.py",
)
assert _SPEC and _SPEC.loader
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["authority_half_life"] = _MOD
_SPEC.loader.exec_module(_MOD)
AuthorityError = _MOD.AuthorityError
AuthorityHalfLife = _MOD.AuthorityHalfLife


SECRET = b"megamind-local-authority-half-life-v1-test-only"


def test_issue_and_verify_fresh_token() -> None:
    auth = AuthorityHalfLife(SECRET, half_life_s=60.0)
    now = 1_700_000_000.0
    tok = auth.issue("verification_unit", "registry.scan", now=now)
    ok, reason = auth.verify(tok, agent_id="verification_unit", command="registry.scan", now=now + 1)
    assert ok is True
    assert reason is None
    fire = auth.authorize_fire(tok, agent_id="verification_unit", command="registry.scan", now=now + 1)
    assert fire["ok"] is True
    assert fire["remaining_fraction"] > 0.9


def test_expired_token_refuses() -> None:
    auth = AuthorityHalfLife(SECRET, half_life_s=10.0)
    now = 1_700_000_000.0
    tok = auth.issue("agent_a", "mesh.connect", now=now)
    ok, reason = auth.verify(tok, now=now + 11)
    assert ok is False
    assert reason == "EXPIRED"
    fire = auth.authorize_fire(tok, agent_id="agent_a", command="mesh.connect", now=now + 11)
    assert fire["ok"] is False
    assert fire["refuse"] == "EXPIRED"


def test_forged_mac_refuses() -> None:
    auth = AuthorityHalfLife(SECRET, half_life_s=60.0)
    tok = auth.issue("agent_a", "cmd")
    forged = type(tok)(**{**tok.to_dict(), "mac": "0" * 64})
    ok, reason = auth.verify(forged)
    assert ok is False
    assert reason == "BAD_MAC"


def test_agent_and_command_binding() -> None:
    auth = AuthorityHalfLife(SECRET, half_life_s=60.0)
    tok = auth.issue("agent_a", "cmd.x")
    assert auth.verify(tok, agent_id="agent_b")[1] == "AGENT_MISMATCH"
    assert auth.verify(tok, command="cmd.y")[1] == "COMMAND_MISMATCH"


def test_roundtrip_dict() -> None:
    auth = AuthorityHalfLife(SECRET, half_life_s=30.0)
    tok = auth.issue("agent_a", "cmd")
    restored = type(tok).from_dict(tok.to_dict())
    assert auth.verify(restored)[0] is True


def test_rejects_empty_secret_and_fields() -> None:
    with pytest.raises(AuthorityError):
        AuthorityHalfLife(b"")
    auth = AuthorityHalfLife(SECRET)
    with pytest.raises(AuthorityError):
        auth.issue("", "cmd")
    with pytest.raises(AuthorityError):
        auth.issue("agent", "")
