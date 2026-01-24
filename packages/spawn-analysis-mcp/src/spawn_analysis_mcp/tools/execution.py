"""
Execution Tools - MCP tools for running spawn-analysis.

Tools:
- conduct_analysis: Start a new analysis session
- add_analyst_result: Submit an analyst's result to a session
- get_analysis_status: Check status of a running analysis
"""

from typing import Optional, List
from fastmcp import FastMCP
from spawn_analysis_mcp.analysis_engine import get_engine
from spawn_analysis_mcp.analyst_registry import get_registry


def register_execution_tools(mcp: FastMCP):
    """
    Register execution tools with FastMCP.

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def conduct_analysis(
        question: str,
        context: str = "",
        analyst_ids: Optional[List[str]] = None,
        analyst_set: str = "general",
        prior_confidence: float = 0.5,
        user_id: str = "default_user",
    ) -> dict:
        """
        Start a new spawn-analysis session.

        Creates an analysis session and returns the analyst prompts that need
        to be executed. Use Claude's Task tool to run analysts in parallel.

        Args:
            question (str): The decision question to analyze
            context (str): Additional context (Vikunja data, background, constraints)
            analyst_ids (List[str], optional): Specific analysts to use.
                If None, uses all analysts from the chosen set.
            analyst_set (str): Which analyst set to use:
                - "general": Business/project decision analysts (8 analysts)
                - "software": Software selection analysts (5 analysts)
                Default: "general"
            prior_confidence (float): Starting Bayesian confidence (0.0-1.0).
                Default: 0.5 (uncertain)
            user_id (str): User identifier for privacy/scoping.
                Defaults to "default_user". Sessions are always saved to storage.

        Returns:
            dict: {
                "session_id": str,
                "question": str,
                "context": str,
                "analysts": [str],        # Analyst IDs in execution order
                "analyst_prompts": [      # Prompts ready for Task tool
                    {
                        "analyst_id": str,
                        "analyst_name": str,
                        "order": int,
                        "prompt": str
                    },
                    ...
                ],
                "prior_confidence": float,
                "status": "pending",
                "instructions": str       # How to execute the analysis
            }

        Example:
            >>> session = conduct_analysis(
            ...     question="Should we migrate to React?",
            ...     context="Current: Vue 2. Team size: 3 devs.",
            ...     analyst_ids=["optimizer", "strategist", "probabilist"]
            ... )
            >>> print(session["session_id"])
            >>> for analyst in session["analyst_prompts"]:
            ...     # Spawn Task tool agent with analyst["prompt"]
            ...     pass
        """
        engine = get_engine()
        registry = get_registry(analyst_set=analyst_set)

        # Create analysis session with specific registry
        session = engine.conduct_analysis(
            question=question,
            context=context,
            analyst_ids=analyst_ids,
            prior_confidence=prior_confidence,
            user_id=user_id,
            registry=registry,
        )

        # Always save to storage (user_id defaults to "default_user")
        from spawn_analysis_mcp.analysis_storage import get_storage
        storage = get_storage()
        storage.save_session(session)

        # Build analyst prompts for execution
        analyst_prompts = []
        for analyst_id in session.analysts:
            analyst = registry.get_analyst(analyst_id)
            if not analyst:
                continue

            # Construct full prompt with question and context
            full_prompt = f"""You are conducting a spawn-analysis as the {analyst.name}.

DECISION QUESTION:
{question}

CONTEXT:
{context}

ANALYST FRAMEWORK:
{analyst.prompt}

INSTRUCTIONS:
1. Apply the {analyst.name} framework to analyze the decision question
2. Consider the provided context carefully
3. Provide your analysis with clear reasoning
4. End with "Confidence: X%" where X is your confidence level (0-100)

Respond with your complete analysis now.
"""

            analyst_prompts.append(
                {
                    "analyst_id": analyst.id,
                    "analyst_name": analyst.name,
                    "order": analyst.order,
                    "prompt": full_prompt,
                }
            )

        return {
            "session_id": session.session_id,
            "question": session.question,
            "context": session.context,
            "analysts": session.analysts,
            "analyst_prompts": analyst_prompts,
            "prior_confidence": prior_confidence,
            "status": session.status,
            "instructions": (
                "Execute analysts in parallel using Task tool. "
                "Submit each result with add_analyst_result(). "
                "Check progress with get_analysis_status()."
            ),
        }

    @mcp.tool()
    def add_analyst_result(
        session_id: str,
        analyst_id: str,
        analysis: str,
        tokens_input: Optional[int] = None,
        tokens_output: Optional[int] = None,
    ) -> dict:
        """
        Submit an analyst's result to an analysis session.

        Call this after each analyst completes their analysis.
        The engine will extract confidence values automatically.

        Args:
            session_id (str): Session identifier from conduct_analysis()
            analyst_id (str): Analyst identifier (e.g., "optimizer")
            analysis (str): The analyst's complete analysis text
            tokens_input (int, optional): Input tokens consumed by this analyst
            tokens_output (int, optional): Output tokens generated by this analyst

        Returns:
            dict: {
                "session_id": str,
                "analyst_id": str,
                "analyst_name": str,
                "confidence": float or None,
                "tokens_input": int or None,
                "tokens_output": int or None,
                "results_count": int,
                "total_analysts": int,
                "status": str,              # pending, running, completed
                "message": str
            }

        Raises:
            ValueError: If session_id not found or analyst_id invalid

        Example:
            >>> result = add_analyst_result(
            ...     session_id="analysis-20260123-142030",
            ...     analyst_id="optimizer",
            ...     analysis="Analysis text with Confidence: 75%"
            ... )
            >>> print(f"Submitted: {result['analyst_name']}")
            >>> print(f"Progress: {result['results_count']}/{result['total_analysts']}")
        """
        engine = get_engine()

        # Add result to session (with token tracking)
        session = engine.add_analyst_result(
            session_id=session_id,
            analyst_id=analyst_id,
            analysis=analysis,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
        )

        # Always save to storage (sessions always have user_id now)
        from spawn_analysis_mcp.analysis_storage import get_storage
        storage = get_storage()
        storage.save_session(session)

        analyst = get_registry().get_analyst(analyst_id)
        analyst_name = analyst.name if analyst else analyst_id

        # Get confidence from latest result
        latest_result = session.results[-1] if session.results else None
        confidence = latest_result.confidence if latest_result else None

        return {
            "session_id": session.session_id,
            "analyst_id": analyst_id,
            "analyst_name": analyst_name,
            "confidence": confidence,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "results_count": len(session.results),
            "total_analysts": len(session.analysts),
            "status": session.status,
            "message": (
                f"Submitted {analyst_name} result. "
                f"Progress: {len(session.results)}/{len(session.analysts)}"
            ),
        }

    @mcp.tool()
    def get_analysis_status(session_id: str) -> dict:
        """
        Get the current status of an analysis session.

        Returns progress, results, and confidence evolution.

        Args:
            session_id (str): Session identifier from conduct_analysis()

        Returns:
            dict: {
                "session_id": str,
                "question": str,
                "status": str,                    # pending, running, completed
                "results_count": int,
                "total_analysts": int,
                "completed_analysts": [str],
                "pending_analysts": [str],
                "confidence_evolution": [
                    {"analyst": str, "confidence": float},
                    ...
                ],
                "final_confidence": float or None,
                "started_at": str,
                "completed_at": str or None
            }

        Raises:
            ValueError: If session_id not found

        Example:
            >>> status = get_analysis_status("analysis-20260123-142030")
            >>> print(f"Status: {status['status']}")
            >>> print(f"Progress: {status['results_count']}/{status['total_analysts']}")
            >>> print(f"Final confidence: {status['final_confidence']}")
        """
        engine = get_engine()
        session = engine.get_session(session_id)

        if not session:
            raise ValueError(f"Session not found: {session_id}")

        completed_analysts = [r.analyst_id for r in session.results]
        pending_analysts = [
            aid for aid in session.analysts if aid not in completed_analysts
        ]

        return {
            "session_id": session.session_id,
            "question": session.question,
            "status": session.status,
            "results_count": len(session.results),
            "total_analysts": len(session.analysts),
            "completed_analysts": completed_analysts,
            "pending_analysts": pending_analysts,
            "confidence_evolution": [
                {"analyst": analyst, "confidence": conf}
                for analyst, conf in session.confidence_evolution
            ],
            "final_confidence": session.final_confidence,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
        }
