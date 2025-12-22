# S1 Rapid Discovery: Bot SDK Frameworks

**Date**: 2025-12-22
**Methodology**: S1 - Rapid practical comparison
**Category**: 1.234 (Bot SDK Frameworks)
**Scope**: Task management bot development for open social platforms

---

## Executive Summary

For building a task management bot (slash commands, interactive buttons, Vikunja integration):

| Platform | Recommended SDK | Time to MVP | Complexity |
|----------|-----------------|-------------|------------|
| **Matrix** | matrix-nio (Python) | 4-8 hours | Medium |
| **Discord** | discord.py | 2-4 hours | Low |
| **Telegram** | python-telegram-bot | 2-4 hours | Low |
| **Nostr** | nostr-tools (JS) | 4-8 hours | Medium |
| **Slack** | slack-bolt | 4-8 hours | Medium |

**Recommendation**: For Factumerit with Matrix target, use **matrix-nio** (Python) - same language as existing Vikunja bot, excellent async support, full feature access.

---

## Matrix Bot SDKs

### matrix-nio (Python) ⭐ Recommended

**Overview**: Async Python SDK for Matrix, supports E2EE.

**Installation**:
```bash
pip install matrix-nio[e2e]
```

**Basic Bot Example**:
```python
import asyncio
from nio import AsyncClient, RoomMessageText

class TaskBot:
    def __init__(self, homeserver, user_id, password):
        self.client = AsyncClient(homeserver, user_id)
        self.password = password

    async def message_callback(self, room, event):
        if event.body.startswith("!tasks"):
            # Parse command
            args = event.body.split()[1:]

            if not args or args[0] == "today":
                tasks = await self.get_vikunja_tasks("today")
                response = self.format_tasks(tasks)
            elif args[0] == "add":
                task_title = " ".join(args[1:])
                await self.create_vikunja_task(task_title)
                response = f"✅ Created: {task_title}"
            else:
                response = "Commands: !tasks [today|overdue|add <title>]"

            await self.client.room_send(
                room.room_id,
                "m.room.message",
                {"msgtype": "m.text", "body": response}
            )

    async def run(self):
        await self.client.login(self.password)
        self.client.add_event_callback(self.message_callback, RoomMessageText)
        await self.client.sync_forever(timeout=30000)

# Run
bot = TaskBot("https://matrix.org", "@taskbot:matrix.org", "password")
asyncio.run(bot.run())
```

**Features**:
| Feature | Support |
|---------|---------|
| Text commands | ✅ Native |
| Slash commands | ❌ Not protocol-native (use `!` prefix) |
| Interactive buttons | ⚠️ Via widgets (complex) |
| Reactions | ✅ Native |
| E2E Encryption | ✅ Full support |
| File uploads | ✅ Native |
| Typing indicators | ✅ Native |
| Read receipts | ✅ Native |

**Strengths**:
- Async-first design
- E2EE support built-in
- Well-documented
- Active maintenance
- Python ecosystem (same as existing bot)

**Weaknesses**:
- No native slash commands (Matrix protocol limitation)
- Interactive buttons require widget complexity
- Learning curve for Matrix concepts (rooms, events)

**Time to MVP**: 4-8 hours

---

### matrix-bot-sdk (TypeScript)

**Overview**: Official TypeScript SDK for Matrix bots.

**Installation**:
```bash
npm install matrix-bot-sdk
```

**Basic Example**:
```typescript
import { MatrixClient, SimpleFsStorageProvider, AutojoinRoomsMixin } from "matrix-bot-sdk";

const client = new MatrixClient(
    "https://matrix.org",
    "access_token",
    new SimpleFsStorageProvider("bot.json")
);

AutojoinRoomsMixin.setupOnClient(client);

client.on("room.message", async (roomId, event) => {
    if (event.content.body?.startsWith("!tasks")) {
        const tasks = await getVikunjaTasks();
        await client.sendText(roomId, formatTasks(tasks));
    }
});

client.start().then(() => console.log("Bot started"));
```

**Strengths**:
- TypeScript types
- Official SDK
- Good for JS ecosystem

**Weaknesses**:
- Different language from existing Python bot
- Slightly less documentation than nio

**Time to MVP**: 4-8 hours

---

## Discord Bot SDKs

### discord.py (Python) ⭐ Recommended for Discord

**Overview**: Most popular Python Discord library, excellent slash command support.

**Installation**:
```bash
pip install discord.py
```

**Slash Commands Example**:
```python
import discord
from discord import app_commands

class TaskBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = TaskBot()

@client.tree.command(name="tasks", description="Show your tasks")
@app_commands.describe(filter="Filter: today, overdue, all")
async def tasks(interaction: discord.Interaction, filter: str = "today"):
    tasks = await get_vikunja_tasks(filter)

    embed = discord.Embed(title=f"📋 Tasks ({filter})", color=0x00ff00)
    for task in tasks[:10]:
        embed.add_field(name=task.title, value=task.due_date or "No due date", inline=False)

    await interaction.response.send_message(embed=embed)

@client.tree.command(name="add", description="Add a new task")
@app_commands.describe(title="Task title", due="Due date (optional)")
async def add_task(interaction: discord.Interaction, title: str, due: str = None):
    task = await create_vikunja_task(title, due)
    await interaction.response.send_message(f"✅ Created: {title}")

client.run("BOT_TOKEN")
```

**Interactive Buttons Example**:
```python
class TaskView(discord.ui.View):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

    @discord.ui.button(label="✅ Complete", style=discord.ButtonStyle.success)
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await complete_vikunja_task(self.task_id)
        await interaction.response.edit_message(content="Task completed!", view=None)

    @discord.ui.button(label="⏰ Snooze", style=discord.ButtonStyle.secondary)
    async def snooze(self, interaction: discord.Interaction, button: discord.ui.Button):
        await snooze_vikunja_task(self.task_id)
        await interaction.response.edit_message(content="Snoozed 1 day", view=None)

# Usage
@client.tree.command(name="task", description="View a task")
async def view_task(interaction: discord.Interaction, task_id: int):
    task = await get_vikunja_task(task_id)
    view = TaskView(task_id)
    await interaction.response.send_message(f"**{task.title}**\n{task.description}", view=view)
```

**Features**:
| Feature | Support |
|---------|---------|
| Slash commands | ✅ Excellent (native) |
| Interactive buttons | ✅ Excellent (Views) |
| Dropdowns/Selects | ✅ Native |
| Modals/Forms | ✅ Native |
| Embeds | ✅ Rich formatting |
| File uploads | ✅ Native |
| Reactions | ✅ Native |

**Strengths**:
- Best slash command UX
- Excellent interactive components
- Large community
- Well-documented
- Same language as existing bot

**Weaknesses**:
- Requires bot verification for >100 servers
- No self-hosting (Discord is centralized)
- Gaming reputation

**Time to MVP**: 2-4 hours

---

### discord.js (JavaScript)

**Similar features to discord.py, use if JS preferred.**

**Time to MVP**: 2-4 hours

---

## Telegram Bot SDKs

### python-telegram-bot ⭐ Recommended for Telegram

**Overview**: Feature-complete Python wrapper for Telegram Bot API.

**Installation**:
```bash
pip install python-telegram-bot
```

**Commands Example**:
```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = await get_vikunja_tasks("today")

    keyboard = []
    for task in tasks[:5]:
        keyboard.append([
            InlineKeyboardButton(f"✅ {task.title}", callback_data=f"complete_{task.id}"),
            InlineKeyboardButton("⏰", callback_data=f"snooze_{task.id}")
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 Today's Tasks:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action, task_id = query.data.split("_")

    if action == "complete":
        await complete_vikunja_task(task_id)
        await query.answer("Task completed!")
    elif action == "snooze":
        await snooze_vikunja_task(task_id)
        await query.answer("Snoozed 1 day")

    await query.edit_message_text("Updated!")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = " ".join(context.args)
    if not title:
        await update.message.reply_text("Usage: /add <task title>")
        return

    await create_vikunja_task(title)
    await update.message.reply_text(f"✅ Created: {title}")

app = Application.builder().token("BOT_TOKEN").build()
app.add_handler(CommandHandler("tasks", tasks))
app.add_handler(CommandHandler("add", add))
app.add_handler(CallbackQueryHandler(button_callback))
app.run_polling()
```

**Features**:
| Feature | Support |
|---------|---------|
| Slash commands | ✅ Native (`/command`) |
| Inline keyboards | ✅ Excellent |
| Reply keyboards | ✅ Native |
| Inline mode | ✅ Native |
| File uploads | ✅ Native |
| Location sharing | ✅ Native |
| Mini Apps | ✅ WebApp support |

**Strengths**:
- Best mobile experience
- Excellent inline keyboards
- Simple API
- Large user base (900M)
- Fast development

**Weaknesses**:
- Centralized (Telegram controls)
- No self-hosting
- Ick factor (Russia association)

**Time to MVP**: 2-4 hours

---

## Nostr Bot SDKs

### nostr-tools (JavaScript)

**Overview**: Core JavaScript library for Nostr protocol.

**Installation**:
```bash
npm install nostr-tools
```

**Bot Example**:
```javascript
import { SimplePool, getPublicKey, finalizeEvent } from 'nostr-tools';

const sk = "private_key_hex";
const pk = getPublicKey(sk);
const pool = new SimplePool();

const relays = [
    'wss://relay.damus.io',
    'wss://relay.nostr.band',
    'wss://nos.lol'
];

// Subscribe to mentions
const sub = pool.subscribeMany(relays, [{
    kinds: [1],
    '#p': [pk],
    since: Math.floor(Date.now() / 1000)
}], {
    onevent(event) {
        if (event.content.includes('!tasks')) {
            handleTaskCommand(event);
        }
    }
});

async function handleTaskCommand(event) {
    const tasks = await getVikunjaTasks();
    const response = formatTasks(tasks);

    const replyEvent = finalizeEvent({
        kind: 1,
        created_at: Math.floor(Date.now() / 1000),
        tags: [
            ['e', event.id],
            ['p', event.pubkey]
        ],
        content: response
    }, sk);

    await Promise.all(relays.map(r => pool.publish([r], replyEvent)));
}
```

**Features**:
| Feature | Support |
|---------|---------|
| Text commands | ✅ Via mentions |
| Slash commands | ❌ Not protocol-native |
| Interactive buttons | ❌ Not supported |
| Reactions | ✅ Kind 7 events |
| Zaps (payments) | ✅ NIP-57 |
| E2E encryption | ❌ (relays see content) |

**Strengths**:
- Censorship resistant
- Lightning payments native
- Simple protocol
- No platform approval needed

**Weaknesses**:
- No interactive components
- Smaller user base
- Key management complexity
- No slash commands

**Time to MVP**: 4-8 hours

---

## Slack Bot SDK (Reference)

### slack-bolt (Python)

**Current implementation baseline.**

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token="xoxb-...")

@app.command("/tasks")
def handle_tasks(ack, command, client):
    ack()
    tasks = get_vikunja_tasks()
    blocks = format_task_blocks(tasks)
    client.chat_postMessage(channel=command["channel_id"], blocks=blocks)

@app.action("complete_task")
def handle_complete(ack, body, client):
    ack()
    task_id = body["actions"][0]["value"]
    complete_vikunja_task(task_id)
    client.chat_update(...)

handler = SocketModeHandler(app, "xapp-...")
handler.start()
```

**Features**:
| Feature | Support |
|---------|---------|
| Slash commands | ✅ Excellent |
| Interactive buttons | ✅ Block Kit |
| Modals | ✅ Native |
| Rich formatting | ✅ Block Kit |

**Weaknesses**:
- Per-user cost ($8.75/mo)
- Admin API gated
- TOS restrictions

---

## Feature Comparison Matrix

| Feature | Matrix (nio) | Discord.py | Telegram | Nostr | Slack |
|---------|--------------|------------|----------|-------|-------|
| **Slash commands** | ❌ `!` prefix | ✅ Native | ✅ Native | ❌ | ✅ Native |
| **Interactive buttons** | ⚠️ Widgets | ✅ Views | ✅ Inline KB | ❌ | ✅ Block Kit |
| **Dropdowns** | ⚠️ Widgets | ✅ Native | ✅ Native | ❌ | ✅ Native |
| **Modals/Forms** | ❌ | ✅ Native | ❌ | ❌ | ✅ Native |
| **Rich embeds** | ⚠️ HTML | ✅ Embeds | ✅ Markdown | ❌ | ✅ Blocks |
| **E2E encryption** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Self-hosting** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Payments** | ❌ | ❌ | ❌ | ✅ Zaps | ❌ |
| **Python SDK** | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| **Time to MVP** | 4-8h | 2-4h | 2-4h | 4-8h | 4-8h |

---

## Recommendation for Factumerit

### Primary: matrix-nio (Python)

**Why**:
1. Same language as existing Slack bot (easy port)
2. Full E2E encryption support
3. Self-hostable
4. Vikunja ecosystem alignment
5. Bridge compatibility (can reach Slack users)

**Trade-off**: No native slash commands or interactive buttons. Use `!command` syntax and text-based menus.

### Migration Path from Slack

```
Current Slack Bot (slack-bolt)
         ↓
    Port to matrix-nio
         ↓
    !tasks instead of /tasks
    Text menus instead of buttons
         ↓
    Bridge to Slack (mautrix-slack)
         ↓
    Slack users see Matrix bot responses
```

### Recommended Implementation

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
        # Get tasks from Vikunja
        resp = await self.vikunja.get("/api/v1/tasks")
        tasks = resp.json()

        # Format response
        lines = ["📋 **Your Tasks**\n"]
        for i, task in enumerate(tasks[:10], 1):
            status = "✅" if task["done"] else "⬜"
            lines.append(f"{i}. {status} {task['title']}")

        await self.send(room.room_id, "\n".join(lines))

    async def cmd_add(self, room, event, body):
        title = body[5:].strip()
        if not title:
            await self.send(room.room_id, "Usage: !add <task title>")
            return

        await self.vikunja.put("/api/v1/projects/1/tasks", json={"title": title})
        await self.send(room.room_id, f"✅ Added: {title}")

    async def cmd_done(self, room, event, body):
        task_id = body[6:].strip()
        await self.vikunja.post(f"/api/v1/tasks/{task_id}", json={"done": True})
        await self.send(room.room_id, f"✅ Completed task {task_id}")

    async def cmd_help(self, room, event):
        help_text = """**Factumerit Bot Commands**

!tasks - Show your tasks
!add <title> - Add a new task
!done <id> - Mark task complete
!help - Show this help"""
        await self.send(room.room_id, help_text)

    async def send(self, room_id, message):
        await self.client.room_send(
            room_id, "m.room.message",
            {"msgtype": "m.text", "body": message, "format": "org.matrix.custom.html"}
        )

    async def run(self):
        await self.client.login(self.password)
        self.client.add_event_callback(self.handle_message, RoomMessageText)
        await self.client.sync_forever(timeout=30000)

# Run
bot = FactumeritBot(
    homeserver="https://matrix.example.com",
    user_id="@factumerit:example.com",
    password="...",
    vikunja_url="https://vikunja.example.com",
    vikunja_token="..."
)
asyncio.run(bot.run())
```

---

## Sources

- [matrix-nio documentation](https://matrix-nio.readthedocs.io/)
- [discord.py documentation](https://discordpy.readthedocs.io/)
- [python-telegram-bot docs](https://python-telegram-bot.readthedocs.io/)
- [nostr-tools GitHub](https://github.com/nbd-wtf/nostr-tools)
- [Slack Bolt documentation](https://slack.dev/bolt-python/)
