#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(base_url='https://app.vikunja.cloud', token='tk_b58cb267d291c55985136b9f054a62e0502e803f')
task = client.tasks.get(int(sys.argv[1]))

print(f'ID: {task.id}')
print(f'Title: {task.title}')
print(f'Project: {task.project_id}')
print(f'\nDescription:')
print(task.description or '(none)')
