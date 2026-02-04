# 22: Bot SDK Evaluation for Factumerit

**Date**: 2025-12-22
**Status**: DECIDED
**Decision**: matrix-nio (Python)
**Research**: 1.234 Bot SDK Frameworks

---

## Context

Factumerit needs a bot SDK for Vikunja task management integration on Matrix platform (per decision in doc 21).

**Constraints**:
- Target platform: Matrix (self-hosted Dendrite)
- Existing codebase: Python (Slack bot)
- Single user (no bridge needed)

---

## SDK Selection

### Chosen: matrix-nio (Python)

**Why**:
1. Same language as existing Slack bot (easy port)
2. Full E2E encryption support
3. Async-first design
4. Well-documented, actively maintained
5. Vikunja community uses Matrix

**Trade-off accepted**: No native slash commands (use `!command` prefix)

### Alternative considered: matrix-bot-sdk (TypeScript)

Rejected - would require language switch from Python.

---

## Migration Path

```
Current Slack Bot (slack-bolt)
         ↓
    Port to matrix-nio
         ↓
    !tasks instead of /tasks
    Text menus instead of buttons
         ↓
    Deploy on same Render instance
```

---

## Implementation Reference

```python
# Factumerit Matrix Bot - Minimal Viable Implementation
import asyncio
from nio import AsyncClient, RoomMessageText
import httpx

class FactumeritBot:
    def __init__(self, homeserver, user_id, password, vikunja_url, vikunja_token):
        self.client = AsyncClient(homeserver, user_id)
        self.password = password
        self.vikunja = httpx.AsyncClient(
            base_url=vikunja_url,
            headers={"Authorization": f"Bearer {vikunja_token}"}
        )

    async def handle_message(self, room, event):
        body = event.body.strip()

        if body.startswith("!tasks"):
            await self.cmd_tasks(room, event, body)
        elif body.startswith("!add"):
            await self.cmd_add(room, event, body)
        elif body.startswith("!done"):
            await self.cmd_done(room, event, body)
        elif body.startswith("!help"):
            await self.cmd_help(room, event)

    async def cmd_tasks(self, room, event, body):
        resp = await self.vikunja.get("/api/v1/tasks")
        tasks = resp.json()

        lines = ["**Your Tasks**\n"]
        for i, task in enumerate(tasks[:10], 1):
            status = "[x]" if task["done"] else "[ ]"
            lines.append(f"{i}. {status} {task['title']}")

        await self.send(room.room_id, "\n".join(lines))

    async def cmd_add(self, room, event, body):
        title = body[5:].strip()
        if not title:
            await self.send(room.room_id, "Usage: !add <task title>")
            return

        await self.vikunja.put("/api/v1/projects/1/tasks", json={"title": title})
        await self.send(room.room_id, f"Added: {title}")

    async def cmd_done(self, room, event, body):
        task_id = body[6:].strip()
        await self.vikunja.post(f"/api/v1/tasks/{task_id}", json={"done": True})
        await self.send(room.room_id, f"Completed task {task_id}")

    async def cmd_help(self, room, event):
        help_text = """**Bot Commands**

!tasks - Show your tasks
!add <title> - Add a new task
!done <id> - Mark task complete
!help - Show this help"""
        await self.send(room.room_id, help_text)

    async def send(self, room_id, message):
        await self.client.room_send(
            room_id, "m.room.message",
            {"msgtype": "m.text", "body": message}
        )

    async def run(self):
        await self.client.login(self.password)
        self.client.add_event_callback(self.handle_message, RoomMessageText)
        await self.client.sync_forever(timeout=30000)
```

---

## Dependencies

- `matrix-nio[e2e]` - Matrix client with E2EE support
- `httpx` - Async HTTP client for Vikunja API

---

## Related

- [21-MATRIX_PLATFORM_RECOMMENDATION.md](21-MATRIX_PLATFORM_RECOMMENDATION.md)
- [1.234 Bot SDK Frameworks Research](../../research/1.234-bot-sdk-frameworks/)
