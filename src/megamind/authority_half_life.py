"""Command Authority Half-life — expiring actuation tokens for mesh commands.

Stale authority cannot fire. Local reference mechanism only — not production
cloud IAM, not live provider authority, not surveillance.

Mechanism: authority_half_life (Library of Links impact land).
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass
from typing import Any


DEFAULT_HALF_LIFE_S = 300.0  # 5 minutes
MIN_HALF_LIFE_S = 1.0
MAX_HALF_LIFE_S = 86_400.0  # 1 day


class AuthorityError(ValueError):
    """Authority issuance or verification failed closed."""


@dataclass(frozen=True)
class AuthorityToken:
    """Cryptographically bound command grant with hard expiry."""

    token_id: str
    agent_id: str
    command: str
    issued_at: float
    expires_at: float
    half_life_s: float
    mac: str
    nonce: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "token_id": self.token_id,
            "agent_id": self.agent_id,
            "command": self.command,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "half_life_s": self.half_life_s,
            "mac": self.mac,
            "nonce": self.nonce,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuthorityToken:
        return cls(
            token_id=str(data["token_id"]),
            agent_id=str(data["agent_id"]),
            command=str(data["command"]),
            issued_at=float(data["issued_at"]),
            expires_at=float(data["expires_at"]),
            half_life_s=float(data["half_life_s"]),
            mac=str(data["mac"]),
            nonce=str(data["nonce"]),
        )


class AuthorityHalfLife:
    """Issue and verify expiring command tokens. Fail closed on stale/forged."""

    def __init__(self, secret: bytes, *, half_life_s: float = DEFAULT_HALF_LIFE_S) -> None:
        if not secret:
            raise AuthorityError("secret required")
        if half_life_s < MIN_HALF_LIFE_S or half_life_s > MAX_HALF_LIFE_S:
            raise AuthorityError(f"half_life_s out of range [{MIN_HALF_LIFE_S}, {MAX_HALF_LIFE_S}]")
        self._secret = secret
        self._half_life_s = float(half_life_s)

    def _mac(self, body: str) -> str:
        return hmac.new(self._secret, body.encode("utf-8"), hashlib.sha256).hexdigest()

    def _body(self, token: AuthorityToken) -> str:
        return (
            f"{token.token_id}|{token.agent_id}|{token.command}|"
            f"{token.issued_at:.6f}|{token.expires_at:.6f}|"
            f"{token.half_life_s:.6f}|{token.nonce}"
        )

    def issue(
        self,
        agent_id: str,
        command: str,
        *,
        now: float | None = None,
        half_life_s: float | None = None,
    ) -> AuthorityToken:
        if not agent_id.strip():
            raise AuthorityError("agent_id required")
        if not command.strip():
            raise AuthorityError("command required")
        hl = float(self._half_life_s if half_life_s is None else half_life_s)
        if hl < MIN_HALF_LIFE_S or hl > MAX_HALF_LIFE_S:
            raise AuthorityError("half_life_s out of range")
        t = time.time() if now is None else float(now)
        token = AuthorityToken(
            token_id=f"ATH-{secrets.token_hex(6).upper()}",
            agent_id=agent_id.strip(),
            command=command.strip(),
            issued_at=t,
            expires_at=t + hl,
            half_life_s=hl,
            mac="",  # filled after body
            nonce=secrets.token_hex(8),
        )
        mac = self._mac(self._body(token))
        return AuthorityToken(
            token_id=token.token_id,
            agent_id=token.agent_id,
            command=token.command,
            issued_at=token.issued_at,
            expires_at=token.expires_at,
            half_life_s=token.half_life_s,
            mac=mac,
            nonce=token.nonce,
        )

    def verify(
        self,
        token: AuthorityToken,
        *,
        agent_id: str | None = None,
        command: str | None = None,
        now: float | None = None,
    ) -> tuple[bool, str | None]:
        t = time.time() if now is None else float(now)
        expected = self._mac(self._body(token))
        if not hmac.compare_digest(expected, token.mac):
            return False, "BAD_MAC"
        if t > token.expires_at:
            return False, "EXPIRED"
        # Half-life remaining fraction (informational refuse if already dead)
        age = t - token.issued_at
        if age < 0:
            return False, "CLOCK_SKEW"
        if agent_id is not None and agent_id != token.agent_id:
            return False, "AGENT_MISMATCH"
        if command is not None and command != token.command:
            return False, "COMMAND_MISMATCH"
        return True, None

    def remaining_fraction(self, token: AuthorityToken, *, now: float | None = None) -> float:
        """1.0 at issue → 0.0 at expiry (and below)."""
        t = time.time() if now is None else float(now)
        if token.half_life_s <= 0:
            return 0.0
        rem = token.expires_at - t
        return max(0.0, min(1.0, rem / token.half_life_s))

    def authorize_fire(
        self,
        token: AuthorityToken,
        *,
        agent_id: str,
        command: str,
        now: float | None = None,
    ) -> dict[str, Any]:
        """Single fail-closed actuation check used by mesh/kernel call sites."""
        ok, reason = self.verify(token, agent_id=agent_id, command=command, now=now)
        return {
            "ok": ok,
            "refuse": None if ok else reason,
            "remaining_fraction": self.remaining_fraction(token, now=now),
            "token_id": token.token_id,
            "plane": "IMPLEMENTED",
            "claim_boundary": "local_reference_not_production_iam",
        }
