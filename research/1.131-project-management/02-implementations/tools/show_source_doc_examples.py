#!/usr/bin/env python3
"""
Show examples of what source document updates would look like.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(base_url='https://app.vikunja.cloud', token='tk_b58cb267d291c55985136b9f054a62e0502e803f')

# Example tasks to show
EXAMPLES = [
    {'task_id': 217408, 'folder': 'inverse-fractional', 'codebase': None},
    {'task_id': 217411, 'folder': 'qrcards', 'codebase': '/home/ivanadmin/qrcards/'},
    {'task_id': 217415, 'folder': 'boutique-hotel-recs', 'codebase': None}
]

print("=" * 80)
print("SOURCE DOCUMENT UPDATE EXAMPLES")
print("=" * 80)
print()

for example in EXAMPLES:
    task = client.tasks.get(example['task_id'])

    print(f"Task: {task.title} (ID: {task.id})")
    print("-" * 80)
    print()
    print("CURRENT DESCRIPTION:")
    print(task.description or "(none)")
    print()
    print("PROPOSED UPDATE:")
    print()

    # Build source document section
    source_docs = f"""
---
<strong>📂 Source Documents for Analysis:</strong><br>
<ul>
<li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/{example['folder']}/vikunja-tasks.yaml</code></li>
<li>Project folder: <code>/home/ivanadmin/spawn-solutions/applications/{example['folder']}/</code></li>
"""

    if example['codebase']:
        source_docs += f"<li>Codebase: <code>{example['codebase']}</code></li>\n"

    source_docs += "</ul>"

    # Append to existing description
    if task.description:
        new_description = task.description + "\n\n" + source_docs
    else:
        new_description = source_docs

    print(new_description)
    print()
    print("=" * 80)
    print()

print("\nThese examples show how source documents would be appended to existing")
print("task descriptions to help spawn-analysis agents find evidence.")
