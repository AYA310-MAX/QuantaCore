"""Local dashboard UI for AyAstra / QuantaCore.

Beginner explanation:
This file starts a tiny local web server using Python's standard library.
A web server is a program that listens for browser requests and sends back
HTML, CSS, JavaScript, or JSON.

This dashboard runs only on your own computer at:

    http://127.0.0.1:8765

It does not expose AyAstra to the public internet.
"""

from __future__ import annotations

import json
import urllib.parse
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from ay_astra.storage.json_store import load_json
from ay_astra.tools.learning import LEARNING_LOG_PATH, add_learning_topic
from ay_astra.tools.news import get_news_brief
from ay_astra.tools.reminders import REMINDERS_PATH, add_reminder
from ay_astra.tools.research import get_research_brief
from ay_astra.tools.tasks import TASKS_PATH, add_task, complete_task

HOST = "127.0.0.1"
PORT = 8765


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the local dashboard."""

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        if path == "/":
            self._send_html(DASHBOARD_HTML)
            return

        if path == "/api/state":
            self._send_json(build_dashboard_state())
            return

        if path == "/api/news":
            topic = query.get("topic", ["technology"])[0]
            self._send_json({"text": get_news_brief(topic)})
            return

        if path == "/api/research":
            topic = query.get("topic", [""])[0]
            self._send_json({"text": get_research_brief(topic)})
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        payload = self._read_json_body()

        if path == "/api/task/add":
            message = add_task(str(payload.get("description", "")))
            self._send_json({"message": message, "state": build_dashboard_state()})
            return

        if path == "/api/task/done":
            message = complete_task(str(payload.get("id", "")))
            self._send_json({"message": message, "state": build_dashboard_state()})
            return

        if path == "/api/learn/add":
            topic = str(payload.get("topic", "")).strip()
            note = str(payload.get("note", "")).strip()
            raw_text = f"{topic} | {note}" if note else topic
            message = add_learning_topic(raw_text)
            self._send_json({"message": message, "state": build_dashboard_state()})
            return

        if path == "/api/reminder/add":
            date_time = str(payload.get("datetime", "")).strip().replace("T", " ")
            message_text = str(payload.get("message", "")).strip()
            message = add_reminder(date_time, message_text)
            self._send_json({"message": message, "state": build_dashboard_state()})
            return

        self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format: str, *args: Any) -> None:
        """Reduce noisy request logs in the terminal."""

        return

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0") or 0)

        if content_length <= 0:
            return {}

        raw_body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            return {}

        return data if isinstance(data, dict) else {}

    def _send_html(self, html: str, status: int = 200) -> None:
        encoded = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        encoded = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def build_dashboard_state() -> dict[str, Any]:
    """Read JSON storage files and return dashboard state."""

    tasks = load_json(TASKS_PATH, [])
    reminders = load_json(REMINDERS_PATH, [])
    learning_log = load_json(LEARNING_LOG_PATH, [])

    pending_tasks = [task for task in tasks if not task.get("done")]
    completed_tasks = [task for task in tasks if task.get("done")]
    pending_reminders = [reminder for reminder in reminders if not reminder.get("delivered")]
    total_reviews = sum(int(entry.get("times_reviewed", 0) or 0) for entry in learning_log)

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stats": {
            "tasks_total": len(tasks),
            "tasks_pending": len(pending_tasks),
            "tasks_done": len(completed_tasks),
            "reminders_total": len(reminders),
            "reminders_pending": len(pending_reminders),
            "learning_topics": len(learning_log),
            "learning_reviews": total_reviews,
        },
        "tasks": tasks,
        "reminders": reminders,
        "learning_log": learning_log,
        "project_root": str(Path.cwd()),
    }


def run_dashboard(host: str = HOST, port: int = PORT, open_browser: bool = True) -> None:
    """Run the local dashboard server."""

    server = ThreadingHTTPServer((host, port), DashboardHandler)
    url = f"http://{host}:{port}"

    print("AyAstra Dashboard online — QuantaCore lab interface active.")
    print(f"Open: {url}")
    print("Press Ctrl+C in this terminal to stop the dashboard.")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard shutting down. Lab lights dimmed.")
    finally:
        server.server_close()


DASHBOARD_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AyAstra / QuantaCore Dashboard</title>
  <style>
    :root {
      --bg: #050816;
      --panel: rgba(14, 22, 48, 0.86);
      --panel-strong: rgba(18, 32, 68, 0.94);
      --line: rgba(103, 232, 249, 0.28);
      --text: #e5f7ff;
      --muted: #95a9c8;
      --cyan: #67e8f9;
      --blue: #60a5fa;
      --violet: #a78bfa;
      --gold: #fbbf24;
      --green: #34d399;
      --red: #fb7185;
      --shadow: 0 0 30px rgba(103, 232, 249, 0.16);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      background:
        radial-gradient(circle at 20% 10%, rgba(96, 165, 250, 0.28), transparent 30%),
        radial-gradient(circle at 90% 0%, rgba(167, 139, 250, 0.22), transparent 34%),
        radial-gradient(circle at 50% 100%, rgba(52, 211, 153, 0.14), transparent 28%),
        var(--bg);
      font-family: Inter, Segoe UI, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: 0.12;
      background-image:
        linear-gradient(rgba(103,232,249,0.2) 1px, transparent 1px),
        linear-gradient(90deg, rgba(103,232,249,0.2) 1px, transparent 1px);
      background-size: 42px 42px;
      mask-image: linear-gradient(to bottom, black, transparent 90%);
    }

    .shell {
      width: min(1280px, calc(100% - 28px));
      margin: 0 auto;
      padding: 24px 0 42px;
    }

    header {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 18px;
      align-items: center;
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: 26px;
      background: linear-gradient(135deg, rgba(14,22,48,0.9), rgba(10,15,35,0.72));
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }

    header::after {
      content: "";
      position: absolute;
      width: 280px;
      height: 280px;
      right: -120px;
      top: -140px;
      border: 1px solid rgba(103,232,249,0.35);
      border-radius: 50%;
      box-shadow: 0 0 60px rgba(103,232,249,0.18) inset;
    }

    h1, h2, h3, p { margin-top: 0; }

    h1 {
      margin-bottom: 6px;
      letter-spacing: -0.04em;
      font-size: clamp(2rem, 5vw, 4.6rem);
      line-height: 0.95;
    }

    .gradient-text {
      background: linear-gradient(90deg, var(--cyan), var(--blue), var(--violet));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }

    .subtitle {
      color: var(--muted);
      margin-bottom: 0;
      max-width: 780px;
      line-height: 1.6;
    }

    .status-pill {
      justify-self: end;
      padding: 12px 16px;
      border: 1px solid rgba(52, 211, 153, 0.38);
      border-radius: 999px;
      color: #d1fae5;
      background: rgba(6, 78, 59, 0.25);
      box-shadow: 0 0 20px rgba(52, 211, 153, 0.12);
      white-space: nowrap;
      z-index: 1;
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin: 18px 0;
    }

    .stat, .panel {
      border: 1px solid var(--line);
      border-radius: 22px;
      background: var(--panel);
      box-shadow: var(--shadow);
      backdrop-filter: blur(14px);
    }

    .stat {
      padding: 18px;
      min-height: 112px;
    }

    .stat .label {
      color: var(--muted);
      font-size: 0.86rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }

    .stat .value {
      font-size: 2.5rem;
      font-weight: 800;
      margin-top: 8px;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }

    .panel {
      padding: 18px;
      min-height: 280px;
    }

    .wide { grid-column: span 2; }

    .panel h2 {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      font-size: 1.05rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #cffafe;
    }

    .tag {
      color: var(--gold);
      font-size: 0.78rem;
      font-weight: 700;
    }

    .list {
      display: grid;
      gap: 10px;
      max-height: 370px;
      overflow: auto;
      padding-right: 4px;
    }

    .item {
      border: 1px solid rgba(103,232,249,0.18);
      border-radius: 16px;
      padding: 12px;
      background: rgba(8, 13, 30, 0.62);
    }

    .item.done {
      opacity: 0.58;
    }

    .item-title {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 10px;
      font-weight: 700;
    }

    .meta {
      color: var(--muted);
      font-size: 0.86rem;
      margin-top: 6px;
      line-height: 1.45;
    }

    form, .control-row {
      display: grid;
      gap: 8px;
      margin: 12px 0 16px;
    }

    input, button, textarea {
      width: 100%;
      border: 1px solid rgba(103,232,249,0.26);
      border-radius: 14px;
      background: rgba(3, 7, 18, 0.76);
      color: var(--text);
      padding: 12px 13px;
      font: inherit;
      outline: none;
    }

    input:focus, textarea:focus {
      border-color: var(--cyan);
      box-shadow: 0 0 0 3px rgba(103,232,249,0.12);
    }

    button {
      cursor: pointer;
      border: none;
      color: #03121d;
      font-weight: 800;
      background: linear-gradient(90deg, var(--cyan), var(--blue));
      transition: transform 0.18s ease, filter 0.18s ease;
    }

    button:hover { transform: translateY(-1px); filter: brightness(1.08); }

    button.secondary {
      color: var(--text);
      border: 1px solid rgba(103,232,249,0.22);
      background: rgba(103,232,249,0.08);
    }

    button.danger {
      color: #fff1f2;
      background: linear-gradient(90deg, #fb7185, #f97316);
    }

    .two { grid-template-columns: 1fr 1fr; }

    pre {
      white-space: pre-wrap;
      word-break: break-word;
      color: #dffbff;
      background: rgba(3, 7, 18, 0.72);
      border: 1px solid rgba(103,232,249,0.16);
      border-radius: 16px;
      padding: 14px;
      max-height: 420px;
      overflow: auto;
      line-height: 1.5;
    }

    .toast {
      position: fixed;
      left: 50%;
      bottom: 24px;
      transform: translateX(-50%);
      width: min(720px, calc(100% - 28px));
      padding: 14px 16px;
      border-radius: 16px;
      border: 1px solid rgba(103,232,249,0.35);
      background: var(--panel-strong);
      box-shadow: var(--shadow);
      color: var(--text);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
      z-index: 20;
    }

    .toast.show { opacity: 1; }

    @media (max-width: 950px) {
      header { grid-template-columns: 1fr; }
      .status-pill { justify-self: start; }
      .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .grid { grid-template-columns: 1fr; }
      .wide { grid-column: auto; }
      .two { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div>
        <h1><span class="gradient-text">AyAstra</span><br/>QuantaCore Lab</h1>
        <p class="subtitle">
          Your local command center for tasks, reminders, learning, news and research.
          Still not a full Wakanda lab, but we are absolutely being dramatic in the correct direction.
        </p>
      </div>
      <div class="status-pill" id="statusPill">Systems loading...</div>
    </header>

    <section class="stats">
      <div class="stat"><div class="label">Pending Tasks</div><div class="value" id="tasksPending">0</div></div>
      <div class="stat"><div class="label">Reminders</div><div class="value" id="remindersPending">0</div></div>
      <div class="stat"><div class="label">Learning Topics</div><div class="value" id="learningTopics">0</div></div>
      <div class="stat"><div class="label">Reviews</div><div class="value" id="learningReviews">0</div></div>
    </section>

    <section class="grid">
      <div class="panel">
        <h2>Tasks <span class="tag">Planner</span></h2>
        <form id="taskForm">
          <input id="taskInput" placeholder="Add a task, e.g. Finish AI assignment" />
          <button>Add Task</button>
        </form>
        <div class="list" id="tasksList"></div>
      </div>

      <div class="panel">
        <h2>Reminders <span class="tag">Timeline</span></h2>
        <form id="reminderForm">
          <input id="reminderDate" type="datetime-local" />
          <input id="reminderMessage" placeholder="Reminder message" />
          <button>Add Reminder</button>
        </form>
        <div class="list" id="remindersList"></div>
      </div>

      <div class="panel">
        <h2>Learning Log <span class="tag">Archive</span></h2>
        <form id="learnForm">
          <input id="learnTopic" placeholder="Topic, e.g. APIs" />
          <textarea id="learnNote" rows="3" placeholder="Note, e.g. APIs let apps talk"></textarea>
          <button>Add Learning Topic</button>
        </form>
        <div class="list" id="learningList"></div>
      </div>

      <div class="panel wide">
        <h2>Verified News <span class="tag">Source-backed</span></h2>
        <div class="control-row two">
          <input id="newsTopic" value="ai" placeholder="Topic, e.g. ai, tech, south africa" />
          <button id="newsButton">Fetch News</button>
        </div>
        <pre id="newsOutput">Click “Fetch News” to load source-backed headlines.</pre>
      </div>

      <div class="panel">
        <h2>Research Mode <span class="tag">Academic</span></h2>
        <div class="control-row">
          <input id="researchTopic" value="AI agents in education" placeholder="Research topic" />
          <button id="researchButton">Search Papers</button>
        </div>
        <pre id="researchOutput">Search a research topic to load paper metadata and links.</pre>
      </div>
    </section>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    const $ = (id) => document.getElementById(id);

    function escapeHtml(value) {
      return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
    }

    function showToast(message) {
      const toast = $('toast');
      toast.textContent = message;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3600);
    }

    async function apiGet(url) {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      return response.json();
    }

    async function apiPost(url, body) {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      return response.json();
    }

    async function refreshState() {
      const state = await apiGet('/api/state');
      renderState(state);
    }

    function renderState(state) {
      $('statusPill').textContent = `Local systems online • ${state.generated_at}`;
      $('tasksPending').textContent = state.stats.tasks_pending;
      $('remindersPending').textContent = state.stats.reminders_pending;
      $('learningTopics').textContent = state.stats.learning_topics;
      $('learningReviews').textContent = state.stats.learning_reviews;

      renderTasks(state.tasks || []);
      renderReminders(state.reminders || []);
      renderLearning(state.learning_log || []);
    }

    function renderTasks(tasks) {
      const container = $('tasksList');
      if (!tasks.length) {
        container.innerHTML = `<div class="item"><div class="meta">No tasks yet. Suspiciously peaceful.</div></div>`;
        return;
      }

      container.innerHTML = tasks.map(task => `
        <div class="item ${task.done ? 'done' : ''}">
          <div class="item-title">
            <span>${task.done ? '✅' : '⬜'} #${task.id}: ${escapeHtml(task.description)}</span>
            ${task.done ? '' : `<button class="secondary" onclick="completeTask(${task.id})">Done</button>`}
          </div>
          <div class="meta">Created: ${escapeHtml(task.created_at || 'unknown')}</div>
        </div>
      `).join('');
    }

    function renderReminders(reminders) {
      const container = $('remindersList');
      if (!reminders.length) {
        container.innerHTML = `<div class="item"><div class="meta">No reminders yet. Timeline clean.</div></div>`;
        return;
      }

      container.innerHTML = reminders.map(reminder => `
        <div class="item ${reminder.delivered ? 'done' : ''}">
          <div class="item-title">
            <span>${reminder.delivered ? '✅' : '⏰'} #${reminder.id}: ${escapeHtml(reminder.message)}</span>
          </div>
          <div class="meta">When: ${escapeHtml(remu(reminder.remind_at))}</div>
        </div>
      `).join('');
    }

    function remu(value) { return value || 'unknown'; }

    function renderLearning(entries) {
      const container = $('learningList');
      if (!entries.length) {
        container.innerHTML = `<div class="item"><div class="meta">Learning log empty. Add a topic and feed the archive.</div></div>`;
        return;
      }

      container.innerHTML = entries.map(entry => `
        <div class="item">
          <div class="item-title"><span>#${entry.id}: ${escapeHtml(entry.topic)}</span></div>
          <div class="meta">${escapeHtml(entry.note || 'No note saved')}</div>
          <div class="meta">Reviews: ${entry.times_reviewed || 0} • Last reviewed: ${escapeHtml(entry.last_reviewed_at || 'never')}</div>
        </div>
      `).join('');
    }

    async function completeTask(id) {
      const data = await apiPost('/api/task/done', { id });
      showToast(data.message);
      renderState(data.state);
    }

    $('taskForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const description = $('taskInput').value.trim();
      if (!description) return showToast('Task description missing. Even futuristic dashboards need details.');
      const data = await apiPost('/api/task/add', { description });
      $('taskInput').value = '';
      showToast(data.message);
      renderState(data.state);
    });


    $('reminderForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const datetime = $('reminderDate').value.trim();
      const message = $('reminderMessage').value.trim();
      if (!datetime || !message) return showToast('Reminder needs a date/time and message. Precision, Ayanda.');
      const data = await apiPost('/api/reminder/add', { datetime, message });
      $('reminderMessage').value = '';
      showToast(data.message);
      renderState(data.state);
    });

    $('learnForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const topic = $('learnTopic').value.trim();
      const note = $('learnNote').value.trim();
      if (!topic) return showToast('Learning topic missing. The archive cannot store vibes only.');
      const data = await apiPost('/api/learn/add', { topic, note });
      $('learnTopic').value = '';
      $('learnNote').value = '';
      showToast(data.message);
      renderState(data.state);
    });

    $('newsButton').addEventListener('click', async () => {
      const topic = $('newsTopic').value.trim() || 'technology';
      $('newsOutput').textContent = 'Fetching source-backed headlines...';
      try {
        const data = await apiGet(`/api/news?topic=${encodeURIComponent(topic)}`);
        $('newsOutput').textContent = data.text;
      } catch (error) {
        $('newsOutput').textContent = `News fetch failed: ${error.message}`;
      }
    });

    $('researchButton').addEventListener('click', async () => {
      const topic = $('researchTopic').value.trim();
      if (!topic) return showToast('Research topic missing. Even scholars need a question.');
      $('researchOutput').textContent = 'Searching academic metadata...';
      try {
        const data = await apiGet(`/api/research?topic=${encodeURIComponent(topic)}`);
        $('researchOutput').textContent = data.text;
      } catch (error) {
        $('researchOutput').textContent = `Research search failed: ${error.message}`;
      }
    });

    refreshState().catch((error) => showToast(`Dashboard load failed: ${error.message}`));
    setInterval(refreshState, 15000);
  </script>
</body>
</html>
"""
