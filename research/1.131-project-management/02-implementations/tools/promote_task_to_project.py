#!/usr/bin/env python3
"""
Promote Task to Sub-Project

Generic pattern for graduating a task to a full sub-project when commitment increases.

Pattern:
  Lightweight task → Heavy sub-project when:
  - Idea becomes serious
  - Lead becomes client
  - Concept becomes build
  - Topic becomes research

Usage:
    python3 promote_task_to_project.py <task_id> [--template TEMPLATE]

Templates:
    - talk: Speaking engagement (proposal, slides, delivery, follow-up)
    - research: Research investigation (discovery, analysis, synthesis, report)
    - product: Product development (design, build, test, launch)
    - client: Client engagement (discovery, proposal, delivery, closure)
    - custom: Basic project (todo, doing, done)

Example:
    python3 promote_task_to_project.py 216450 --template talk
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

# Sub-project task templates
TASK_TEMPLATES = {
    'talk': {
        'description': 'Speaking engagement preparation tasks',
        'tasks': [
            {"title": "Research topic and outline", "priority": 5},
            {"title": "Write abstract and proposal", "priority": 5},
            {"title": "Submit to CFP", "priority": 4},
            {"title": "Create slide deck", "priority": 3},
            {"title": "Build demos/examples", "priority": 3},
            {"title": "Rehearse presentation", "priority": 2},
            {"title": "Deliver talk", "priority": 1},
            {"title": "Create follow-up materials", "priority": 1},
        ],
        'next_stage': {
            'from': '💡 Ideas',
            'to': '📝 Proposal Writing'
        }
    },
    'research': {
        'description': 'Research investigation tasks',
        'tasks': [
            {"title": "Define research question", "priority": 5},
            {"title": "Literature review", "priority": 4},
            {"title": "Collect data/evidence", "priority": 4},
            {"title": "Analyze findings", "priority": 3},
            {"title": "Synthesize conclusions", "priority": 2},
            {"title": "Write report", "priority": 1},
            {"title": "Publish/share findings", "priority": 1},
        ],
        'next_stage': {
            'from': 'Ideas',
            'to': 'In Progress'
        }
    },
    'product': {
        'description': 'Product development tasks',
        'tasks': [
            {"title": "Define requirements", "priority": 5},
            {"title": "Design architecture", "priority": 5},
            {"title": "Create mockups/wireframes", "priority": 4},
            {"title": "Build core features", "priority": 4},
            {"title": "Write tests", "priority": 3},
            {"title": "User testing", "priority": 2},
            {"title": "Launch", "priority": 1},
            {"title": "Post-launch monitoring", "priority": 1},
        ],
        'next_stage': {
            'from': 'Backlog',
            'to': 'In Progress'
        }
    },
    'client': {
        'description': 'Client engagement tasks',
        'tasks': [
            {"title": "Initial discovery call", "priority": 5},
            {"title": "Understand requirements", "priority": 5},
            {"title": "Write proposal", "priority": 4},
            {"title": "Negotiate contract", "priority": 4},
            {"title": "Deliver work", "priority": 3},
            {"title": "Review and revisions", "priority": 2},
            {"title": "Invoice and close", "priority": 1},
        ],
        'next_stage': {
            'from': 'Leads',
            'to': 'Active'
        }
    },
    'custom': {
        'description': 'Custom project tasks',
        'tasks': [
            {"title": "Plan the work", "priority": 5},
            {"title": "Do the work", "priority": 3},
            {"title": "Review and complete", "priority": 1},
        ],
        'next_stage': {
            'from': 'Todo',
            'to': 'Doing'
        }
    },
}


def promote_task_to_project(task_id: int, template: str = 'custom',
                           source_folder: str = None, codebase: str = None,
                           dry_run: bool = False):
    """
    Promote a task to a full sub-project.

    Args:
        task_id: ID of task to promote
        template: Template for sub-project tasks
        source_folder: Relative path to project folder in applications/
        codebase: Absolute path to codebase (if applicable)
        dry_run: If True, show plan without creating
    """

    if template not in TASK_TEMPLATES:
        print(f"❌ Unknown template: {template}")
        print(f"Available templates: {', '.join(TASK_TEMPLATES.keys())}")
        return False

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)
    template_config = TASK_TEMPLATES[template]

    print("=" * 80)
    print("PROMOTING TASK TO SUB-PROJECT")
    print("=" * 80)

    # Get the task
    try:
        task = client.tasks.get(task_id)
    except Exception as e:
        print(f"❌ Failed to get task {task_id}: {e}")
        return False

    print(f"\nOriginal Task:")
    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Project: {task.project_id}")
    print(f"  Description: {task.description[:100] if task.description else '(none)'}...")
    print()

    # Get parent project
    try:
        parent_project = client.projects.get(task.project_id)
        print(f"Parent Project: {parent_project.title} (ID: {parent_project.id})")
    except Exception as e:
        print(f"❌ Failed to get parent project: {e}")
        return False

    # Plan the promotion
    subproject_title = task.title
    subproject_description = f"""
{task.description or ''}

<br><br>
<strong>Promoted from task #{task.id}</strong><br>
Original pipeline position: {parent_project.title}<br>
<br>
<strong>Linked task:</strong> <a href="https://app.vikunja.cloud/tasks/{task.id}">View main tracking task</a>
""".strip()

    print()
    print("=" * 80)
    print("PROMOTION PLAN")
    print("=" * 80)
    print(f"\n📦 Create Sub-Project:")
    print(f"   Title: {subproject_title}")
    print(f"   Parent: {parent_project.title}")
    print(f"   Template: {template}")
    print()

    print(f"📋 Create {len(template_config['tasks'])} tasks:")
    for t in template_config['tasks']:
        priority_str = f"P{t['priority']}" if t['priority'] > 0 else ""
        print(f"   - {t['title']} {priority_str}")
    print()

    print(f"🔗 Update original task:")
    print(f"   - Add link to new sub-project")
    print(f"   - Update description with promotion note")
    print()

    next_stage = template_config.get('next_stage')
    if next_stage:
        print(f"📊 Pipeline movement (suggested):")
        print(f"   {next_stage['from']} → {next_stage['to']}")
        print()

    if dry_run:
        print("=" * 80)
        print("DRY RUN - No changes made")
        print("=" * 80)
        print("\nTo execute, run without --dry-run flag")
        return True

    # Execute promotion
    print("=" * 80)
    print("EXECUTING PROMOTION")
    print("=" * 80)
    print()

    try:
        # 1. Create sub-project
        print("1. Creating sub-project...")
        subproject = client.projects.create(
            title=subproject_title,
            description=template_config['description'],
            parent_project_id=parent_project.id
        )
        print(f"   ✅ Created: {subproject.title} (ID: {subproject.id})")
        print(f"   📂 View: https://app.vikunja.cloud/projects/{subproject.id}")
        print()

        # 2. Create tasks in sub-project
        print(f"2. Creating {len(template_config['tasks'])} tasks...")
        created_tasks = []
        for task_def in template_config['tasks']:
            try:
                new_task = client.tasks.create(
                    project_id=subproject.id,
                    title=task_def['title'],
                    priority=task_def.get('priority', 0)
                )
                print(f"   ✅ {new_task.title}")
                created_tasks.append(new_task)
            except Exception as e:
                print(f"   ⚠️  Failed to create '{task_def['title']}': {e}")
        print()

        # 3. Update original task
        print("3. Updating original task...")
        updated_description = f"""
{task.description or ''}

<br><br>
<strong>📦 Promoted to Sub-Project</strong><br>
Details: <a href="https://app.vikunja.cloud/projects/{subproject.id}">View sub-project</a><br>
Tasks: {len(created_tasks)} implementation tasks<br>
Template: {template}
""".strip()

        # Add source documents if provided
        if source_folder:
            source_docs = f"""

---
<strong>📂 Source Documents for Analysis:</strong><br>
<ul>
<li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/{source_folder}/vikunja-tasks.yaml</code></li>
<li>Project folder: <code>/home/ivanadmin/spawn-solutions/applications/{source_folder}/</code></li>
"""
            if codebase:
                source_docs += f"<li>Codebase: <code>{codebase}</code></li>\n"
            source_docs += "</ul>"

            updated_description += source_docs.strip()
            print(f"   ✅ Added source document references")

        client.tasks.update(
            task_id=task.id,
            description=updated_description
        )
        print(f"   ✅ Added link to sub-project")
        print()

        # 4. Summary
        print("=" * 80)
        print("PROMOTION COMPLETE")
        print("=" * 80)
        print()
        print("✅ Created:")
        print(f"   Sub-project: {subproject.title} (ID: {subproject.id})")
        print(f"   Tasks: {len(created_tasks)}")
        print()
        print("🔗 Links:")
        print(f"   Main task: https://app.vikunja.cloud/tasks/{task.id}")
        print(f"   Sub-project: https://app.vikunja.cloud/projects/{subproject.id}")
        print()

        if next_stage:
            print("💡 Suggested next step:")
            print(f"   Move main task from '{next_stage['from']}' to '{next_stage['to']}'")
            print()

        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ Promotion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Promote task to sub-project (generic pattern)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Templates:
  talk      Speaking engagement (proposal → delivery → follow-up)
  research  Research investigation (discovery → analysis → report)
  product   Product development (design → build → launch)
  client    Client engagement (discovery → delivery → closure)
  custom    Basic project (plan → do → review)

Pattern:
  1. Task exists in main project kanban (lightweight tracking)
  2. Promote to sub-project when commitment increases
  3. Sub-project contains detailed implementation tasks
  4. Main task stays in kanban for pipeline visibility
  5. When done: mark main task complete, archive sub-project

Source Documents:
  Use --source-folder and --codebase to add references for spawn-analysis agents.
  This helps AI agents find evidence when making decisions about priorities.

Examples:
  # Dry run to see what will happen
  python3 promote_task_to_project.py 216450 --template talk --dry-run

  # Execute promotion
  python3 promote_task_to_project.py 216450 --template talk

  # Promote with source documents for spawn-analysis
  python3 promote_task_to_project.py 216450 --template product \\
      --source-folder qrcards --codebase /home/ivanadmin/qrcards/

  # Site project (no codebase, just planning docs)
  python3 promote_task_to_project.py 216451 --template custom \\
      --source-folder inverse-fractional

  # Custom template
  python3 promote_task_to_project.py 216450 --template custom
        """
    )
    parser.add_argument('task_id', type=int, help='ID of task to promote')
    parser.add_argument('--template', '-t', default='custom',
                        choices=list(TASK_TEMPLATES.keys()),
                        help='Sub-project template (default: custom)')
    parser.add_argument('--source-folder', '-s',
                        help='Relative path to project folder in applications/ (e.g., "qrcards")')
    parser.add_argument('--codebase', '-c',
                        help='Absolute path to codebase (e.g., "/home/ivanadmin/qrcards/")')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show plan without executing')

    args = parser.parse_args()

    success = promote_task_to_project(
        args.task_id,
        args.template,
        args.source_folder,
        args.codebase,
        args.dry_run
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
