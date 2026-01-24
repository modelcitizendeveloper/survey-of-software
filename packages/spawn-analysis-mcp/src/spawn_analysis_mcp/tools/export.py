"""
Export Tools - MCP tools for exporting analysis results.

Phase 2.1: Basic markdown export
Phase 2.2: JSON export (added)
Phase 2.3: Vikunja export, HTML export
Phase 3: QRCards integration

Tools:
- save_analysis: Export analysis to markdown, JSON, or HTML file
- export_to_vikunja_task: Create Vikunja task with analysis results
"""

import json
import os
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from spawn_analysis_mcp.analysis_engine import get_engine
import requests


def register_export_tools(mcp: FastMCP):
    """
    Register export tools with FastMCP.

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def save_analysis(
        session_id: str,
        output_path: str,
        format: str = "markdown",
    ) -> dict:
        """
        Save analysis results to a file.

        Phase 2.1: Markdown export
        Phase 2.2: JSON export (added)
        Phase 2.3: HTML export (added)
        Phase 3: QRCards export

        Args:
            session_id (str): Session identifier from conduct_analysis()
            output_path (str): Path where to save the analysis
            format (str): Output format: "markdown", "json", or "html"

        Returns:
            dict: {
                "session_id": str,
                "output_path": str,
                "format": str,
                "file_size": int,
                "message": str
            }

        Raises:
            ValueError: If session not found or format unsupported

        Example:
            >>> result = save_analysis(
            ...     session_id="analysis-20260123-142030",
            ...     output_path="/tmp/decision-analysis.md"
            ... )
            >>> print(f"Saved to: {result['output_path']}")
            >>> print(f"Size: {result['file_size']} bytes")
        """
        engine = get_engine()
        session = engine.get_session(session_id)

        if not session:
            raise ValueError(f"Session not found: {session_id}")

        if format not in ("markdown", "json", "html"):
            raise ValueError(
                f"Unsupported format: {format}. "
                f"Supported: markdown, json, html"
            )

        # Generate output based on format
        if format == "markdown":
            content = _generate_markdown_report(session)
        elif format == "json":
            content = json.dumps(session.to_dict(), indent=2)
        elif format == "html":
            content = _generate_html_report(session)

        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding="utf-8")

        return {
            "session_id": session.session_id,
            "output_path": str(output_file),
            "format": format,
            "file_size": len(content),
            "message": f"Analysis saved to {output_file}",
        }


def _generate_markdown_report(session) -> str:
    """
    Generate a markdown report from an analysis session.

    Args:
        session: AnalysisSession object

    Returns:
        Markdown-formatted report
    """
    lines = []

    # Header
    lines.append(f"# Spawn-Analysis: {session.question}")
    lines.append("")
    lines.append(f"**Session ID**: {session.session_id}")
    lines.append(f"**Status**: {session.status}")
    lines.append(f"**Started**: {session.started_at}")
    if session.completed_at:
        lines.append(f"**Completed**: {session.completed_at}")
    lines.append("")

    # Context
    if session.context:
        lines.append("## Context")
        lines.append("")
        lines.append(session.context)
        lines.append("")

    # Confidence Evolution
    if session.confidence_evolution:
        lines.append("## Confidence Evolution")
        lines.append("")
        lines.append("| Analyst | Confidence |")
        lines.append("|---------|------------|")
        for analyst, confidence in session.confidence_evolution:
            conf_pct = f"{confidence*100:.0f}%" if confidence else "N/A"
            lines.append(f"| {analyst} | {conf_pct} |")
        lines.append("")

    # Analyst Results
    lines.append("## Analyst Perspectives")
    lines.append("")

    for i, result in enumerate(session.results, 1):
        lines.append(f"### {i}. {result.analyst_name}")
        lines.append("")
        if result.confidence:
            lines.append(f"**Confidence**: {result.confidence*100:.0f}%")
            lines.append("")
        lines.append(result.analysis)
        lines.append("")
        lines.append("---")
        lines.append("")

    # Summary
    if session.final_confidence is not None:
        lines.append("## Summary")
        lines.append("")
        lines.append(f"**Final Confidence**: {session.final_confidence*100:.0f}%")
        lines.append(
            f"**Analysts Consulted**: {len(session.results)}/{len(session.analysts)}"
        )
        lines.append("")

    return "\n".join(lines)


    @mcp.tool()
    def export_to_vikunja_task(
        session_id: str,
        project_id: int,
        user_id: str,
        task_title: Optional[str] = None,
        vikunja_url: Optional[str] = None,
        vikunja_token: Optional[str] = None,
    ) -> dict:
        """
        Create a Vikunja task with analysis results.

        Creates a task in the specified Vikunja project with:
        - Title: Decision question or custom task_title
        - Description: Executive summary of analysis
        - Comment: Full analysis markdown report
        - Label: "spawn-analysis" (auto-created if needed)

        Requires Vikunja credentials via parameters or environment:
        - VIKUNJA_URL: Vikunja instance URL
        - VIKUNJA_TOKEN: API token from Vikunja Settings > API Tokens

        Args:
            session_id (str): Session identifier from conduct_analysis()
            project_id (int): Vikunja project ID where task will be created
            user_id (str): User ID for privacy enforcement
            task_title (str, optional): Custom task title (default: use question)
            vikunja_url (str, optional): Vikunja instance URL (default: from env)
            vikunja_token (str, optional): Vikunja API token (default: from env)

        Returns:
            dict: {
                "task_id": int,
                "task_title": str,
                "project_id": int,
                "url": str,
                "label_created": bool
            }

        Raises:
            ValueError: If session not found or Vikunja credentials missing
            RuntimeError: If Vikunja API call fails

        Example:
            >>> result = export_to_vikunja_task(
            ...     session_id="analysis-20260123-142030",
            ...     project_id=123,
            ...     user_id="user@example.com"
            ... )
            >>> print(f"Created task: {result['url']}")
        """
        from spawn_analysis_mcp.analysis_storage import get_storage

        # Get credentials
        url = vikunja_url or os.environ.get("VIKUNJA_URL")
        token = vikunja_token or os.environ.get("VIKUNJA_TOKEN")

        if not url or not token:
            raise ValueError(
                "Vikunja credentials required. "
                "Provide vikunja_url/vikunja_token or set "
                "VIKUNJA_URL/VIKUNJA_TOKEN environment variables."
            )

        # Remove trailing slash from URL
        url = url.rstrip("/")

        # Get session (enforces user_id privacy)
        storage = get_storage()
        session = storage.get_analysis(session_id, user_id)

        if not session:
            raise ValueError(
                f"Session '{session_id}' not found for user '{user_id}'"
            )

        # Prepare task data
        title = task_title or session.question
        summary = _generate_executive_summary(session)
        full_report = _generate_markdown_report(session)

        # Create task
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        task_data = {
            "title": title,
            "description": summary,
            "project_id": project_id,
        }

        response = requests.post(
            f"{url}/api/v1/projects/{project_id}/tasks",
            json=task_data,
            headers=headers,
            timeout=30,
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Failed to create Vikunja task: {response.status_code} "
                f"{response.text}"
            )

        task = response.json()
        task_id = task["id"]

        # Add full report as comment
        comment_data = {"comment": f"## Full Analysis Report\n\n{full_report}"}

        comment_response = requests.put(
            f"{url}/api/v1/tasks/{task_id}/comments",
            json=comment_data,
            headers=headers,
            timeout=30,
        )

        if comment_response.status_code not in (200, 201):
            # Don't fail if comment creation fails - task was created
            print(f"Warning: Failed to add comment: {comment_response.status_code}")

        # Ensure "spawn-analysis" label exists
        label_created = False
        label_id = None

        # Get existing labels
        labels_response = requests.get(
            f"{url}/api/v1/labels",
            headers=headers,
            timeout=30,
        )

        if labels_response.status_code == 200:
            labels = labels_response.json()
            for label in labels:
                if label["title"].lower() == "spawn-analysis":
                    label_id = label["id"]
                    break

        # Create label if it doesn't exist
        if not label_id:
            label_data = {
                "title": "spawn-analysis",
                "hex_color": "3498db",  # Blue
            }
            create_label_response = requests.put(
                f"{url}/api/v1/labels",
                json=label_data,
                headers=headers,
                timeout=30,
            )
            if create_label_response.status_code in (200, 201):
                label_id = create_label_response.json()["id"]
                label_created = True

        # Add label to task
        if label_id:
            add_label_response = requests.put(
                f"{url}/api/v1/tasks/{task_id}/labels",
                json={"label_id": label_id},
                headers=headers,
                timeout=30,
            )
            if add_label_response.status_code not in (200, 201):
                print(f"Warning: Failed to add label: {add_label_response.status_code}")

        # Construct task URL
        task_url = f"{url}/tasks/{task_id}"

        return {
            "task_id": task_id,
            "task_title": title,
            "project_id": project_id,
            "url": task_url,
            "label_created": label_created,
        }


def _generate_executive_summary(session) -> str:
    """
    Generate a brief executive summary from analysis session.

    Args:
        session: AnalysisSession object

    Returns:
        Brief summary (2-3 sentences)
    """
    if not session.results:
        return "Analysis in progress - no results yet."

    # Use synthesizer's analysis if available, otherwise first result
    summary_text = None
    for result in session.results:
        if "synthesizer" in result.analyst_name.lower():
            summary_text = result.analysis
            break

    if not summary_text and session.results:
        summary_text = session.results[0].analysis

    # Extract first paragraph or first 300 chars
    if summary_text:
        lines = summary_text.strip().split("\n\n")
        first_para = lines[0] if lines else summary_text
        if len(first_para) > 300:
            first_para = first_para[:297] + "..."
        return first_para

    return "Analysis completed - see full report for details."


def _generate_html_report(session) -> str:
    """
    Generate an HTML report from an analysis session.

    Args:
        session: AnalysisSession object

    Returns:
        HTML-formatted report with embedded CSS
    """
    import html

    # Escape HTML in text content
    question = html.escape(session.question)
    context_html = html.escape(session.context) if session.context else ""

    # Build HTML
    parts = []

    # HTML header with embedded CSS
    parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spawn-Analysis Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 2em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        h3 {
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        .metadata {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }
        .metadata strong { color: #2c3e50; }
        .context {
            background: #fff9e6;
            border-left: 4px solid #f39c12;
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }
        .confidence-chart {
            margin: 20px 0;
        }
        .confidence-bar {
            margin: 8px 0;
            display: flex;
            align-items: center;
        }
        .confidence-label {
            width: 150px;
            font-size: 0.9em;
            color: #555;
        }
        .confidence-track {
            flex: 1;
            height: 24px;
            background: #ecf0f1;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            color: white;
            font-size: 0.85em;
            font-weight: bold;
        }
        .analyst-section {
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }
        .analyst-header {
            background: #34495e;
            color: white;
            padding: 12px 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }
        .analyst-header:hover {
            background: #2c3e50;
        }
        .analyst-body {
            padding: 15px;
            background: #fafafa;
            border-top: 1px solid #ddd;
        }
        .analyst-body.collapsed {
            display: none;
        }
        .collapse-icon {
            font-size: 1.2em;
            transition: transform 0.3s;
        }
        .collapsed .collapse-icon {
            transform: rotate(-90deg);
        }
        .summary-box {
            background: #e8f5e9;
            border-left: 4px solid #2ecc71;
            padding: 20px;
            margin: 20px 0;
        }
        .summary-box h2 {
            margin-top: 0;
            color: #27ae60;
        }
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; padding: 20px; }
            .analyst-body { display: block !important; }
            .collapse-icon { display: none; }
        }
    </style>
    <script>
        function toggleAnalyst(id) {
            const body = document.getElementById('analyst-' + id);
            const header = body.previousElementSibling;
            body.classList.toggle('collapsed');
            header.classList.toggle('collapsed');
        }
    </script>
</head>
<body>
<div class="container">
""")

    # Title
    parts.append(f"<h1>Spawn-Analysis: {question}</h1>")

    # Metadata
    parts.append('<div class="metadata">')
    parts.append(f'<strong>Session ID:</strong> {html.escape(session.session_id)}<br>')
    parts.append(f'<strong>Status:</strong> {html.escape(session.status)}<br>')
    parts.append(f'<strong>Started:</strong> {html.escape(str(session.started_at))}<br>')
    if session.completed_at:
        parts.append(f'<strong>Completed:</strong> {html.escape(str(session.completed_at))}<br>')
    parts.append('</div>')

    # Context
    if context_html:
        parts.append(f'<div class="context">{context_html}</div>')

    # Confidence Evolution
    if session.confidence_evolution:
        parts.append('<h2>Confidence Evolution</h2>')
        parts.append('<div class="confidence-chart">')
        for analyst, confidence in session.confidence_evolution:
            conf_pct = int(confidence * 100) if confidence else 0
            parts.append(f'<div class="confidence-bar">')
            parts.append(f'<div class="confidence-label">{html.escape(analyst)}</div>')
            parts.append(f'<div class="confidence-track">')
            parts.append(f'<div class="confidence-fill" style="width: {conf_pct}%">{conf_pct}%</div>')
            parts.append(f'</div>')
            parts.append(f'</div>')
        parts.append('</div>')

    # Analyst Perspectives (collapsible)
    parts.append('<h2>Analyst Perspectives</h2>')
    for i, result in enumerate(session.results):
        analyst_name = html.escape(result.analyst_name)
        analysis_html = html.escape(result.analysis).replace('\n', '<br>')
        conf_display = f"{int(result.confidence*100)}%" if result.confidence else "N/A"

        parts.append(f'<div class="analyst-section">')
        parts.append(f'<div class="analyst-header collapsed" onclick="toggleAnalyst({i})">')
        parts.append(f'<span><strong>{i+1}. {analyst_name}</strong> (Confidence: {conf_display})</span>')
        parts.append(f'<span class="collapse-icon">▼</span>')
        parts.append(f'</div>')
        parts.append(f'<div id="analyst-{i}" class="analyst-body collapsed">')
        parts.append(f'{analysis_html}')
        parts.append(f'</div>')
        parts.append(f'</div>')

    # Summary
    if session.final_confidence is not None:
        parts.append('<div class="summary-box">')
        parts.append('<h2>Summary</h2>')
        parts.append(f'<p><strong>Final Confidence:</strong> {int(session.final_confidence*100)}%</p>')
        parts.append(f'<p><strong>Analysts Consulted:</strong> {len(session.results)}/{len(session.analysts)}</p>')
        parts.append('</div>')

    # Footer
    parts.append("""
</div>
</body>
</html>
""")

    return "".join(parts)
