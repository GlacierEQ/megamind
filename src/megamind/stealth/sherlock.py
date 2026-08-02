import sqlite3
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional

class StealthSherlock:
    """Stealth Sherlock Alpha Organ: Forensic memory index & context assembly engine."""

    def __init__(self, db_path: str = "/tmp/megamind_sherlock.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    source_uri TEXT,
                    content TEXT,
                    sha256 TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def index_artifact(self, artifact_id: str, source_uri: str, content: str) -> Dict[str, Any]:
        """Index forensic text artifact into Sherlock memory store."""
        sha256_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO artifacts (artifact_id, source_uri, content, sha256)
                VALUES (?, ?, ?, ?)
            """, (artifact_id, source_uri, content, sha256_hash))
            conn.commit()
        return {
            "artifact_id": artifact_id,
            "source_uri": source_uri,
            "sha256": sha256_hash,
            "status": "INDEXED"
        }

    def search_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search indexed artifacts using keyword matching and context ranking."""
        terms = query.lower().split()
        results = []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT artifact_id, source_uri, content, sha256 FROM artifacts")
            for row in cursor.fetchall():
                content_lower = row["content"].lower()
                score = sum(1 for t in terms if t in content_lower)
                if score > 0:
                    results.append({
                        "artifact_id": row["artifact_id"],
                        "source_uri": row["source_uri"],
                        "content": row["content"],
                        "sha256": row["sha256"],
                        "score": score
                    })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
