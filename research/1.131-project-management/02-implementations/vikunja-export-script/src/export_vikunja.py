#!/usr/bin/env python3
"""
Vikunja Portfolio Export Script

Exports current Vikunja portfolio state for spawn-analysis decision input.

Usage:
    python export_vikunja.py                           # Console output
    python export_vikunja.py --format json             # JSON output
    python export_vikunja.py --output portfolio.md     # Save to file
    python export_vikunja.py --spawn-analysis          # Format for spawn-analysis cards
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
from dotenv import load_dotenv

# Add vikunja-api-wrapper to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "vikunja-api-wrapper" / "src"))
from vikunja_wrapper import VikunjaClient


def calculate_velocity(tasks: List[Any], weeks: int = 4) -> Dict[str, Any]:
    """
    Calculate velocity metrics from completed tasks

    Args:
        tasks: List of task objects
        weeks: Number of weeks to look back

    Returns:
        Velocity metrics dict
    """
    cutoff_date = datetime.now() - timedelta(weeks=weeks)

    completed_tasks = [
        t for t in tasks
        if hasattr(t, 'done') and t.done and hasattr(t, 'done_at')
    ]

    recent_completed = [
        t for t in completed_tasks
        if t.done_at and datetime.fromisoformat(str(t.done_at).replace('Z', '+00:00')) > cutoff_date
    ]

    total_tasks = len(tasks)
    completed_count = len(completed_tasks)
    recent_count = len(recent_completed)

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_count,
        "completion_rate": round(completed_count / total_tasks * 100, 1) if total_tasks > 0 else 0,
        f"last_{weeks}_weeks_completed": recent_count,
        "tasks_per_week": round(recent_count / weeks, 1) if weeks > 0 else 0,
    }


def get_task_summary(tasks: List[Any]) -> Dict[str, Any]:
    """
    Summarize task status

    Args:
        tasks: List of task objects

    Returns:
        Task summary dict
    """
    now = datetime.now()

    # Count by status
    total = len(tasks)
    done = sum(1 for t in tasks if hasattr(t, 'done') and t.done)
    pending = total - done

    # Count by due date
    overdue = 0
    due_this_week = 0
    due_next_week = 0

    for task in tasks:
        if not hasattr(task, 'due_date') or not task.due_date or task.done:
            continue

        try:
            due = datetime.fromisoformat(str(task.due_date).replace('Z', '+00:00'))
            days_until_due = (due - now).days

            if days_until_due < 0:
                overdue += 1
            elif days_until_due <= 7:
                due_this_week += 1
            elif days_until_due <= 14:
                due_next_week += 1
        except (ValueError, AttributeError):
            continue

    # Count by priority
    priority_counts = defaultdict(int)
    for task in tasks:
        if hasattr(task, 'priority'):
            priority_counts[task.priority] += 1

    return {
        "total": total,
        "done": done,
        "pending": pending,
        "overdue": overdue,
        "due_this_week": due_this_week,
        "due_next_week": due_next_week,
        "priority_distribution": dict(priority_counts),
    }


def get_project_summary(project: Any, tasks: List[Any]) -> Dict[str, Any]:
    """
    Summarize a single project

    Args:
        project: Project object
        tasks: List of tasks for this project

    Returns:
        Project summary dict
    """
    task_summary = get_task_summary(tasks)
    velocity = calculate_velocity(tasks, weeks=4)

    # Get label distribution
    label_counts = defaultdict(int)
    for task in tasks:
        if hasattr(task, 'labels'):
            for label in task.labels:
                if hasattr(label, 'title'):
                    label_counts[label.title] += 1

    return {
        "id": project.id,
        "title": project.title,
        "description": getattr(project, 'description', None),
        "created": getattr(project, 'created', None),
        "tasks": task_summary,
        "velocity": velocity,
        "labels": dict(label_counts),
    }


def export_portfolio(client: VikunjaClient) -> Dict[str, Any]:
    """
    Export complete portfolio state

    Args:
        client: VikunjaClient instance

    Returns:
        Portfolio data dict
    """
    # Get all projects
    projects = client.projects.list()

    # Get all tasks for each project
    portfolio_data = {
        "exported_at": datetime.now().isoformat(),
        "projects": [],
        "summary": {
            "total_projects": len(projects),
            "total_tasks": 0,
            "total_done": 0,
            "total_pending": 0,
            "total_overdue": 0,
        }
    }

    for project in projects:
        try:
            tasks = client.tasks.list(project_id=project.id)
            project_summary = get_project_summary(project, tasks)
            portfolio_data["projects"].append(project_summary)

            # Update summary
            portfolio_data["summary"]["total_tasks"] += project_summary["tasks"]["total"]
            portfolio_data["summary"]["total_done"] += project_summary["tasks"]["done"]
            portfolio_data["summary"]["total_pending"] += project_summary["tasks"]["pending"]
            portfolio_data["summary"]["total_overdue"] += project_summary["tasks"]["overdue"]
        except Exception as e:
            print(f"Warning: Could not fetch tasks for project {project.title}: {e}", file=sys.stderr)
            continue

    return portfolio_data


def format_spawn_analysis(portfolio: Dict[str, Any]) -> str:
    """
    Format portfolio data for spawn-analysis decision cards

    Args:
        portfolio: Portfolio data dict

    Returns:
        Markdown formatted string for spawn-analysis
    """
    output = []

    output.append("# Current Portfolio State")
    output.append(f"\n**Exported**: {portfolio['exported_at']}\n")

    # Summary
    summary = portfolio['summary']
    output.append("## Portfolio Summary\n")
    output.append(f"- **Active Projects**: {summary['total_projects']}")
    output.append(f"- **Total Tasks**: {summary['total_tasks']}")
    output.append(f"- **Completed**: {summary['total_done']} ({round(summary['total_done']/summary['total_tasks']*100 if summary['total_tasks'] > 0 else 0, 1)}%)")
    output.append(f"- **Pending**: {summary['total_pending']}")
    output.append(f"- **Overdue**: {summary['total_overdue']}\n")

    # Projects
    output.append("## Active Projects\n")

    for project in portfolio['projects']:
        output.append(f"### {project['title']}\n")

        if project['description']:
            output.append(f"*{project['description']}*\n")

        # Task status
        tasks = project['tasks']
        output.append(f"**Tasks**: {tasks['total']} total, {tasks['done']} done, {tasks['pending']} pending")

        if tasks['overdue'] > 0:
            output.append(f"⚠️  **{tasks['overdue']} overdue**")
        if tasks['due_this_week'] > 0:
            output.append(f"📅 {tasks['due_this_week']} due this week")
        if tasks['due_next_week'] > 0:
            output.append(f"📅 {tasks['due_next_week']} due next week")

        output.append("")

        # Velocity
        velocity = project['velocity']
        output.append(f"**Velocity**: {velocity['tasks_per_week']} tasks/week (last 4 weeks)")
        output.append(f"**Completion Rate**: {velocity['completion_rate']}%\n")

        # Labels
        if project['labels']:
            top_labels = sorted(project['labels'].items(), key=lambda x: x[1], reverse=True)[:5]
            output.append("**Top Labels**: " + ", ".join([f"{label} ({count})" for label, count in top_labels]))
            output.append("")

    # Decision context
    output.append("## Context for Decision Cards\n")
    output.append("**Question**: What should I prioritize this week?\n")
    output.append("**Considerations**:")

    # Highlight attention areas
    overdue_projects = [p for p in portfolio['projects'] if p['tasks']['overdue'] > 0]
    if overdue_projects:
        output.append(f"- **{len(overdue_projects)} projects have overdue tasks**")

    stalled_projects = [p for p in portfolio['projects'] if p['velocity']['tasks_per_week'] == 0]
    if stalled_projects:
        output.append(f"- **{len(stalled_projects)} projects have 0 velocity** (no recent completions)")

    active_projects = [p for p in portfolio['projects'] if p['velocity']['tasks_per_week'] > 0]
    if active_projects:
        output.append(f"- **{len(active_projects)} projects are actively progressing**")

    high_workload = [p for p in portfolio['projects'] if p['tasks']['pending'] > 10]
    if high_workload:
        output.append(f"- **{len(high_workload)} projects have >10 pending tasks**")

    return "\n".join(output)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Export Vikunja portfolio state for spawn-analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--format",
        choices=["json", "markdown", "spawn-analysis"],
        default="spawn-analysis",
        help="Output format (default: spawn-analysis)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)"
    )

    parser.add_argument(
        "--spawn-analysis",
        action="store_true",
        help="Format for spawn-analysis decision cards (same as --format spawn-analysis)"
    )

    args = parser.parse_args()

    # Load environment variables
    env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
    if not env_path.exists():
        print(f"Error: .env file not found at: {env_path}", file=sys.stderr)
        sys.exit(1)

    load_dotenv(env_path)

    api_token = os.environ.get("VIKUNJA_API_TOKEN")
    base_url = os.environ.get("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")

    if not api_token:
        print("Error: VIKUNJA_API_TOKEN not found in .env file", file=sys.stderr)
        sys.exit(1)

    # Connect to Vikunja
    try:
        client = VikunjaClient(base_url=base_url, token=api_token)
    except Exception as e:
        print(f"Error: Failed to connect to Vikunja API: {e}", file=sys.stderr)
        sys.exit(1)

    # Export portfolio
    try:
        portfolio = export_portfolio(client)
    except Exception as e:
        print(f"Error: Failed to export portfolio: {e}", file=sys.stderr)
        sys.exit(1)

    # Format output
    if args.spawn_analysis or args.format == "spawn-analysis":
        output = format_spawn_analysis(portfolio)
    elif args.format == "json":
        output = json.dumps(portfolio, indent=2, default=str)
    elif args.format == "markdown":
        output = format_spawn_analysis(portfolio)
    else:
        output = format_spawn_analysis(portfolio)

    # Write output
    if args.output:
        args.output.write_text(output)
        print(f"Portfolio exported to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
