"""
Analysis Storage - User-scoped SQLite storage for analysis sessions.

Provides privacy-enforced storage and retrieval of analysis sessions.
All operations are scoped to user_id to prevent cross-user access.
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from spawn_analysis_mcp.analysis_engine import AnalysisSession, AnalysisResult


class AnalysisStorage:
    """SQLite storage for analysis sessions with user scoping."""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize storage.

        Args:
            db_path: Path to SQLite database. If None, uses storage/analyses.db
        """
        if db_path is None:
            # Default: storage/ next to the package
            module_dir = Path(__file__).parent
            storage_dir = module_dir.parent.parent / "storage"
            storage_dir.mkdir(parents=True, exist_ok=True)
            db_path = storage_dir / "analyses.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                question TEXT NOT NULL,
                context TEXT NOT NULL DEFAULT '',
                analysts TEXT NOT NULL,  -- JSON array
                status TEXT NOT NULL DEFAULT 'pending',
                prior_confidence REAL,
                final_confidence REAL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                token_usage TEXT,  -- JSON object
                total_tokens TEXT,  -- JSON object
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                analyst_id TEXT NOT NULL,
                analyst_name TEXT NOT NULL,
                analysis TEXT NOT NULL,
                confidence REAL,
                tokens_input INTEGER,
                tokens_output INTEGER,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES analyses(session_id)
            )
        """)

        # Confidence evolution table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS confidence_evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                analyst TEXT NOT NULL,
                confidence REAL NOT NULL,
                step_order INTEGER NOT NULL,
                FOREIGN KEY (session_id) REFERENCES analyses(session_id)
            )
        """)

        # Indexes for privacy enforcement and performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analyses_user_id
            ON analyses(user_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analyses_status
            ON analyses(status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_results_session
            ON results(session_id)
        """)

        conn.commit()
        conn.close()

    def save_session(self, session: AnalysisSession) -> bool:
        """
        Save or update an analysis session.

        Args:
            session: AnalysisSession to save

        Returns:
            True if saved successfully

        Raises:
            ValueError: If session has no user_id (privacy enforcement)
        """
        if not session.user_id:
            raise ValueError(
                "Cannot save session without user_id (privacy enforcement)"
            )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Extract prior confidence
            prior_conf = None
            if session.confidence_evolution:
                for analyst, conf in session.confidence_evolution:
                    if analyst == "prior":
                        prior_conf = conf
                        break

            # Save main session record
            cursor.execute("""
                INSERT OR REPLACE INTO analyses
                (session_id, user_id, question, context, analysts, status,
                 prior_confidence, final_confidence, started_at, completed_at,
                 token_usage, total_tokens, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.user_id,
                session.question,
                session.context,
                json.dumps(session.analysts),
                session.status,
                prior_conf,
                session.final_confidence,
                session.started_at,
                session.completed_at,
                json.dumps(session.token_usage) if session.token_usage else None,
                json.dumps(session.total_tokens) if session.total_tokens else None,
                datetime.now().isoformat(),
            ))

            # Clear existing results and confidence evolution
            cursor.execute("DELETE FROM results WHERE session_id = ?",
                         (session.session_id,))
            cursor.execute("DELETE FROM confidence_evolution WHERE session_id = ?",
                         (session.session_id,))

            # Save results
            for result in session.results:
                cursor.execute("""
                    INSERT INTO results
                    (session_id, analyst_id, analyst_name, analysis, confidence,
                     tokens_input, tokens_output, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.session_id,
                    result.analyst_id,
                    result.analyst_name,
                    result.analysis,
                    result.confidence,
                    result.tokens_input,
                    result.tokens_output,
                    result.timestamp,
                ))

            # Save confidence evolution
            for idx, (analyst, confidence) in enumerate(session.confidence_evolution):
                cursor.execute("""
                    INSERT INTO confidence_evolution
                    (session_id, analyst, confidence, step_order)
                    VALUES (?, ?, ?, ?)
                """, (session.session_id, analyst, confidence, idx))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_session(
        self,
        session_id: str,
        user_id: str
    ) -> Optional[AnalysisSession]:
        """
        Get a session by ID (user-scoped).

        Args:
            session_id: Session identifier
            user_id: User identifier (privacy enforcement)

        Returns:
            AnalysisSession or None if not found or access denied
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # Fetch main session (with user_id check for privacy)
            cursor.execute("""
                SELECT * FROM analyses
                WHERE session_id = ? AND user_id = ?
            """, (session_id, user_id))

            row = cursor.fetchone()
            if not row:
                return None

            # Fetch results
            cursor.execute("""
                SELECT * FROM results
                WHERE session_id = ?
                ORDER BY timestamp
            """, (session_id,))

            results = []
            for r in cursor.fetchall():
                results.append(AnalysisResult(
                    analyst_id=r["analyst_id"],
                    analyst_name=r["analyst_name"],
                    analysis=r["analysis"],
                    confidence=r["confidence"],
                    timestamp=r["timestamp"],
                    tokens_input=r["tokens_input"],
                    tokens_output=r["tokens_output"],
                ))

            # Fetch confidence evolution
            cursor.execute("""
                SELECT analyst, confidence FROM confidence_evolution
                WHERE session_id = ?
                ORDER BY step_order
            """, (session_id,))

            confidence_evolution = [
                (row["analyst"], row["confidence"])
                for row in cursor.fetchall()
            ]

            # Reconstruct session
            session = AnalysisSession(
                session_id=row["session_id"],
                question=row["question"],
                context=row["context"],
                analysts=json.loads(row["analysts"]),
                results=results,
                confidence_evolution=confidence_evolution,
                final_confidence=row["final_confidence"],
                started_at=row["started_at"],
                completed_at=row["completed_at"],
                status=row["status"],
                user_id=row["user_id"],
                token_usage=json.loads(row["token_usage"]) if row["token_usage"] else {},
                total_tokens=json.loads(row["total_tokens"]) if row["total_tokens"] else {},
            )

            return session

        finally:
            conn.close()

    def list_sessions(
        self,
        user_id: str,
        limit: int = 50,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List sessions for a user (privacy-enforced).

        Args:
            user_id: User identifier (privacy enforcement)
            limit: Maximum sessions to return
            status: Filter by status (pending, running, completed)

        Returns:
            List of session metadata dicts (not full sessions)
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            query = """
                SELECT session_id, question, status, prior_confidence,
                       final_confidence, started_at, completed_at,
                       total_tokens, updated_at
                FROM analyses
                WHERE user_id = ?
            """
            params = [user_id]

            if status:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY started_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)

            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    "session_id": row["session_id"],
                    "question": row["question"],
                    "status": row["status"],
                    "prior_confidence": row["prior_confidence"],
                    "final_confidence": row["final_confidence"],
                    "started_at": row["started_at"],
                    "completed_at": row["completed_at"],
                    "total_tokens": json.loads(row["total_tokens"]) if row["total_tokens"] else {},
                    "updated_at": row["updated_at"],
                })

            return sessions

        finally:
            conn.close()


# Singleton instance
_storage: Optional[AnalysisStorage] = None


def get_storage() -> AnalysisStorage:
    """
    Get the singleton storage instance.

    Returns:
        AnalysisStorage instance
    """
    global _storage
    if _storage is None:
        _storage = AnalysisStorage()
    return _storage
