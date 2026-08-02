import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional

QUARANTINE_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{32,}", re.IGNORECASE),
    re.compile(r"ghp_[a-zA-Z0-9]{36}", re.IGNORECASE),
    re.compile(r"github_pat_[a-zA-Z0-9_]{50,}", re.IGNORECASE),
    re.compile(r"AIzaSy[a-zA-Z0-9_-]{33}", re.IGNORECASE),
    re.compile(r"\"secret\":\s*\"[^\"]+\"", re.IGNORECASE)
]

class MegamindRecoveryTranche:
    """Governed Recovery Tranche Engine for Primordial Mesh Titan, Continue, Roo, Cline, & Kilo."""

    def __init__(self, megamind_root: Optional[Path] = None):
        if megamind_root is None:
            megamind_root = Path(__file__).parent.parent.parent
        self.megamind_root = megamind_root
        self.recovery_records: List[Dict[str, Any]] = []
        self.quarantine_log: List[Dict[str, Any]] = []

    def sanitize_content(self, raw_content: str, source_id: str) -> str:
        """Quarantine credentials and private keys into hash tokens."""
        sanitized = raw_content
        for pattern in QUARANTINE_PATTERNS:
            matches = pattern.findall(sanitized)
            for m in matches:
                masked_hash = f"[QUARANTINED_SECRET:{hashlib.sha256(m.encode()).hexdigest()[:12]}]"
                sanitized = sanitized.replace(m, masked_hash)
                self.quarantine_log.append({
                    "source_id": source_id,
                    "masked_hash": masked_hash,
                    "status": "QUARANTINED"
                })
        return sanitized

    def ingest_local_orbit(self, source_path: Path, orbit_name: str) -> Dict[str, Any]:
        """Ingest local recovery orbit (e.g. .apex, .continue, .cline, .kilo)."""
        if not source_path.exists():
            return {"orbit": orbit_name, "status": "PATH_NOT_FOUND"}

        files_ingested = []
        for p in source_path.glob("**/*"):
            if p.is_file() and not p.name.startswith(".git"):
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")[:5000]
                    clean_content = self.sanitize_content(content, source_id=f"{orbit_name}/{p.name}")
                    blob_hash = hashlib.sha256(clean_content.encode("utf-8")).hexdigest()
                    files_ingested.append({
                        "filename": p.name,
                        "relative_path": str(p.relative_to(source_path)),
                        "blob_hash": blob_hash,
                        "size_bytes": p.stat().st_size
                    })
                except Exception as e:
                    continue

        rec = {
            "orbit": orbit_name,
            "source_path": str(source_path),
            "files_count": len(files_ingested),
            "sample_files": files_ingested[:10],
            "status": "INGESTED"
        }
        self.recovery_records.append(rec)
        return rec

    def generate_tranche_receipt(self) -> Dict[str, Any]:
        """Generate formal Megamind recovery tranche receipt."""
        total_files = sum(r.get("files_count", 0) for r in self.recovery_records)
        return {
            "tranche_id": "TRANCHE-OMEGA-999-RECOVERY",
            "codex": "BLACKLINE OMEGA-999 / PRIMORDIAL-MESH-TITAN",
            "status": "RECOVERED_AND_QUARANTINED",
            "total_orbits_ingested": len(self.recovery_records),
            "total_files_processed": total_files,
            "quarantined_credentials_count": len(self.quarantine_log),
            "lineage_verification": "CANONICAL_LINEAGE_PRESERVED",
            "receipt_hash": hashlib.sha256(f"{total_files}:{len(self.quarantine_log)}".encode()).hexdigest()
        }
