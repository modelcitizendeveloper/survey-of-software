"""
History Tools - MCP tools for user-scoped analysis history.

All tools enforce user privacy - analyses are scoped to user_id.
No cross-user access is permitted.

Tools:
- list_analyses: List user's analysis history (metadata only)
- get_analysis: Retrieve full analysis session (user-scoped)
"""

from typing import Optional
from fastmcp import FastMCP
from spawn_analysis_mcp.analysis_storage import get_storage


def register_history_tools(mcp: FastMCP):
    """
    Register history tools with FastMCP.

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def list_analyses(
        user_id: str,
        limit: int = 50,
        status: Optional[str] = None,
    ) -> dict:
        """
        List analysis sessions for a user (privacy-enforced).

        Returns metadata only (no full analysis text). Use get_analysis()
        to retrieve complete session data.

        Args:
            user_id (str): User identifier (required for privacy enforcement)
            limit (int): Maximum sessions to return (default: 50, max: 200)
            status (str, optional): Filter by status ("pending", "running", "completed")

        Returns:
            dict: {
                "user_id": str,
                "count": int,
                "analyses": [
                    {
                        "session_id": str,
                        "question": str,
                        "status": str,
                        "prior_confidence": float or None,
                        "final_confidence": float or None,
                        "started_at": str,
                        "completed_at": str or None,
                        "total_tokens": {input: X, output: Y, total: Z},
                        "updated_at": str
                    },
                    ...
                ]
            }

        Example:
            >>> result = list_analyses(user_id="alice@example.com", limit=10)
            >>> print(f"{result['count']} analyses found")
            >>> for analysis in result['analyses']:
            ...     print(f"  {analysis['question'][:50]}...")
        """
        # Enforce max limit
        if limit > 200:
            limit = 200

        storage = get_storage()
        analyses = storage.list_sessions(
            user_id=user_id,
            limit=limit,
            status=status,
        )

        return {
            "user_id": user_id,
            "count": len(analyses),
            "analyses": analyses,
        }

    @mcp.tool()
    def get_analysis(
        session_id: str,
        user_id: str,
    ) -> dict:
        """
        Get a complete analysis session (privacy-enforced).

        Returns full session data including all analyst results.
        Access is restricted to the session owner (user_id).

        Args:
            session_id (str): Session identifier
            user_id (str): User identifier (must match session owner)

        Returns:
            dict: {
                "session_id": str,
                "user_id": str,
                "question": str,
                "context": str,
                "analysts": [str],
                "status": str,
                "results": [
                    {
                        "analyst_id": str,
                        "analyst_name": str,
                        "analysis": str,
                        "confidence": float or None,
                        "tokens_input": int or None,
                        "tokens_output": int or None,
                        "timestamp": str
                    },
                    ...
                ],
                "confidence_evolution": [
                    {"analyst": str, "confidence": float},
                    ...
                ],
                "final_confidence": float or None,
                "started_at": str,
                "completed_at": str or None,
                "token_usage": {analyst_id: {input: X, output: Y}, ...},
                "total_tokens": {input: X, output: Y, total: Z}
            }

        Raises:
            ValueError: If session not found or user_id doesn't match owner

        Example:
            >>> analysis = get_analysis(
            ...     session_id="analysis-20260123-142030",
            ...     user_id="alice@example.com"
            ... )
            >>> print(f"Question: {analysis['question']}")
            >>> print(f"Status: {analysis['status']}")
            >>> print(f"Final confidence: {analysis['final_confidence']}")
            >>> print(f"Total tokens: {analysis['total_tokens']['total']}")
        """
        storage = get_storage()
        session = storage.get_session(session_id=session_id, user_id=user_id)

        if not session:
            raise ValueError(
                f"Analysis '{session_id}' not found or access denied. "
                f"Ensure you own this analysis and the session_id is correct."
            )

        # Convert to dict with proper formatting
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "question": session.question,
            "context": session.context,
            "analysts": session.analysts,
            "status": session.status,
            "results": [
                {
                    "analyst_id": r.analyst_id,
                    "analyst_name": r.analyst_name,
                    "analysis": r.analysis,
                    "confidence": r.confidence,
                    "tokens_input": r.tokens_input,
                    "tokens_output": r.tokens_output,
                    "timestamp": r.timestamp,
                }
                for r in session.results
            ],
            "confidence_evolution": [
                {"analyst": analyst, "confidence": conf}
                for analyst, conf in session.confidence_evolution
            ],
            "final_confidence": session.final_confidence,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
            "token_usage": session.token_usage,
            "total_tokens": session.total_tokens,
        }
