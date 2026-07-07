"""Focused LLM-style chat UI for AyAstra / QuantaCore.

This is NOT a dashboard. It is a Claude/ChatGPT/Siri-inspired chat landing page:
- AyAstra name at the top
- greeting / motivational line in the centre
- large ask box
- quick action chips
- responsive layout for phone, tablet, and desktop browsers

Run locally with:
    python assistant_ui.py

Then open:
    http://127.0.0.1:8765
"""

from __future__ import annotations

import json
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from ay_astra.tools.assistant import handle_message

HOST = "127.0.0.1"
PORT = 8765


class AssistantUIHandler(BaseHTTPRequestHandler):
    """HTTP handler for AyAstra's focused chat UI."""

    def do_GET(self) -> None:  # noqa: N802
        path = urllib.parse.urlparse(self.path).path

        if path == "/":
            self._send_html(ASSISTANT_UI_HTML)
            return

        if path == "/api/health":
            self._send_json({"status": "online", "assistant": "AyAstra", "codename": "QuantaCore"})
            return

        if path == "/manifest.json":
            self._send_json(
                {
                    "name": "AyAstra QuantaCore",
                    "short_name": "AyAstra",
                    "start_url": "/",
                    "display": "standalone",
                    "background_color": "#242620",
                    "theme_color": "#390040",
                    "description": "Ayanda's personal AI assistant chat interface.",
                }
            )
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        path = urllib.parse.urlparse(self.path).path
        payload = self._read_json_body()

        if path == "/api/chat":
            message = str(payload.get("message", "")).strip()

            if not message:
                self._send_json(
                    {
                        "response": "AyAstra: I need words, Ayanda. Even genius interfaces cannot decode decorative silence yet.",
                    }
                )
                return

            response = handle_message(message)
            if response == "__EXIT__":
                response = "AyAstra: The chat interface stays online. Close the tab or stop the server with Ctrl+C."

            self._send_json({"response": response})
            return

        self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format: str, *args: Any) -> None:
        """Keep the terminal clean."""

        return

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}

        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
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


def run_assistant_ui(host: str = HOST, port: int = PORT, open_browser: bool = True) -> None:
    """Start AyAstra's focused assistant UI server."""

    server = ThreadingHTTPServer((host, port), AssistantUIHandler)
    url = f"http://{host}:{port}"

    print("AyAstra Chat UI online — focused assistant interface active.")
    print(f"Open: {url}")
    print("Press Ctrl+C in this terminal to stop the interface.")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAyAstra Chat UI shutting down. QuantaCore resting.")
    finally:
        server.server_close()


ASSISTANT_UI_HTML = r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#242620" />
  <link rel="manifest" href="/manifest.json" />
  <title>AyAstra</title>
  <style>
    :root {
      --bg: #242620;
      --bg-deep: #1b1d18;
      --panel: rgba(255, 255, 255, 0.055);
      --panel-strong: rgba(255, 255, 255, 0.085);
      --line: rgba(255, 255, 255, 0.13);
      --line-strong: rgba(255, 255, 255, 0.2);
      --text: #f4f1eb;
      --muted: rgba(244, 241, 235, 0.58);
      --soft: rgba(244, 241, 235, 0.76);
      --purple: #390040;
      --deep-purple: #1f0035;
      --magenta: #5a0060;
      --gold: #c7940e;
      --navy: #0c111f;
      --rose: #b66570;
      --violet-cloud: #512f5c;
      --peach: #ed9e6f;
      --royal: #2d1f44;
      --plum: #80466e;
      --emerald-deep: #022b22;
      --emerald: #275d46;
      --mint: #569578;
      --accent: #d6785f;
      --accent-2: #c7940e;
      --accent-3: #80466e;
      --safe-bottom: env(safe-area-inset-bottom, 0px);
    }

    * { box-sizing: border-box; }
    html, body { min-height: 100%; }

    body {
      margin: 0;
      min-height: 100dvh;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 50% 12%, rgba(90,0,96,0.15), transparent 22%),
        radial-gradient(circle at 90% 18%, rgba(199,148,14,0.08), transparent 24%),
        radial-gradient(circle at 8% 78%, rgba(39,93,70,0.12), transparent 26%),
        linear-gradient(135deg, #242620 0%, #20221d 48%, #171914 100%);
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        linear-gradient(135deg, transparent 0 48%, rgba(255,255,255,0.025) 49% 51%, transparent 52%),
        radial-gradient(circle at 50% 0%, rgba(255,255,255,0.045), transparent 32%);
      opacity: 0.9;
    }

    .app {
      position: relative;
      z-index: 1;
      width: min(100%, 960px);
      min-height: 100dvh;
      margin: 0 auto;
      display: grid;
      grid-template-rows: auto 1fr auto;
      padding: max(14px, env(safe-area-inset-top, 0px)) clamp(16px, 4vw, 28px) calc(16px + var(--safe-bottom));
    }

    .topbar {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 54px;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--soft);
      font-weight: 760;
      letter-spacing: 0.01em;
    }

    .brand-mark {
      width: 26px;
      height: 26px;
      position: relative;
      animation: markSpin 12s linear infinite;
    }

    .brand-mark::before,
    .brand-mark::after {
      content: "";
      position: absolute;
      inset: 0;
      border-radius: 999px;
      background: conic-gradient(from 0deg, var(--accent), var(--gold), var(--plum), var(--accent));
      clip-path: polygon(50% 0, 60% 34%, 98% 18%, 68% 48%, 100% 58%, 63% 61%, 80% 98%, 50% 70%, 20% 98%, 37% 61%, 0 58%, 32% 48%, 2% 18%, 40% 34%);
      filter: drop-shadow(0 0 14px rgba(214,120,95,0.32));
    }

    .brand-mark::after {
      transform: rotate(22.5deg) scale(0.72);
      opacity: 0.75;
    }

    @keyframes markSpin { to { transform: rotate(360deg); } }

    .main {
      display: grid;
      align-content: center;
      justify-items: center;
      gap: clamp(22px, 4vh, 38px);
      padding: 4vh 0 2vh;
    }

    .hero {
      width: 100%;
      display: grid;
      justify-items: center;
      gap: 14px;
      text-align: center;
      transition: all 0.28s ease;
    }

    .app.has-chat .hero {
      align-self: start;
      gap: 8px;
    }

    .greeting {
      margin: 0;
      max-width: 860px;
      font-family: Georgia, 'Times New Roman', serif;
      font-weight: 420;
      line-height: 1.12;
      letter-spacing: -0.045em;
      color: rgba(244,241,235,0.92);
      font-size: clamp(2.4rem, 8.5vw, 5.35rem);
    }

    .app.has-chat .greeting {
      font-size: clamp(1.55rem, 5vw, 2.4rem);
      opacity: 0.72;
    }

    .quote {
      margin: 0;
      max-width: 700px;
      color: var(--muted);
      line-height: 1.55;
      font-size: clamp(0.98rem, 2.4vw, 1.08rem);
    }

    .chat {
      width: min(100%, 820px);
      display: none;
      gap: 14px;
      padding-bottom: 4px;
    }

    .app.has-chat .chat {
      display: grid;
      align-self: stretch;
      max-height: 48dvh;
      overflow: auto;
      padding-right: 3px;
    }

    .message {
      width: fit-content;
      max-width: min(760px, 94%);
      padding: 14px 16px;
      border-radius: 20px;
      line-height: 1.58;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .message.user {
      justify-self: end;
      background: rgba(255,255,255,0.10);
      border: 1px solid rgba(255,255,255,0.12);
    }

    .message.assistant {
      justify-self: start;
      background: rgba(0,0,0,0.16);
      border: 1px solid rgba(255,255,255,0.10);
    }

    .composer-wrap {
      width: min(100%, 920px);
      margin: 0 auto;
      display: grid;
      gap: 16px;
    }

    .composer {
      min-height: 168px;
      display: grid;
      grid-template-rows: 1fr auto;
      gap: 14px;
      padding: 20px;
      border: 1px solid var(--line-strong);
      border-radius: 30px;
      background: rgba(255,255,255,0.052);
      box-shadow: 0 22px 70px rgba(0,0,0,0.20), inset 0 1px 0 rgba(255,255,255,0.07);
      backdrop-filter: blur(20px);
    }

    textarea {
      width: 100%;
      min-height: 68px;
      resize: none;
      border: 0;
      outline: 0;
      color: var(--text);
      background: transparent;
      font: inherit;
      font-size: clamp(1.1rem, 3vw, 1.35rem);
      line-height: 1.45;
    }

    textarea::placeholder { color: rgba(244,241,235,0.50); }

    .composer-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }

    .left-actions,
    .right-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    button {
      border: 0;
      cursor: pointer;
      color: var(--text);
      font: inherit;
      border-radius: 16px;
      background: rgba(255,255,255,0.055);
      border: 1px solid rgba(255,255,255,0.10);
      transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease;
    }

    button:hover {
      transform: translateY(-1px);
      background: rgba(255,255,255,0.085);
      border-color: rgba(255,255,255,0.18);
    }

    .icon-btn {
      width: 48px;
      height: 48px;
      display: grid;
      place-items: center;
      font-size: 1.4rem;
    }

    .send-btn {
      width: 54px;
      height: 54px;
      display: grid;
      place-items: center;
      color: white;
      background: linear-gradient(135deg, var(--rose), var(--peach));
      border: 0;
      font-size: 1.35rem;
      box-shadow: 0 10px 28px rgba(182,101,112,0.28);
    }

    .model-label {
      color: rgba(244,241,235,0.82);
      font-family: Georgia, 'Times New Roman', serif;
      font-size: clamp(1.05rem, 3vw, 1.3rem);
      white-space: nowrap;
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px 12px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      padding: 12px 18px;
      color: rgba(244,241,235,0.82);
      border-radius: 16px;
      background: rgba(255,255,255,0.035);
      border: 1px solid rgba(255,255,255,0.09);
      font-size: clamp(0.92rem, 2.5vw, 1rem);
    }

    .chip span { opacity: 0.75; }

    .status-line {
      min-height: 22px;
      text-align: center;
      color: var(--muted);
      font-size: 0.88rem;
    }

    .speaking-dot {
      display: none;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 16px var(--accent);
      animation: dotPulse 0.9s ease-in-out infinite;
    }

    .app.thinking .speaking-dot,
    .app.speaking .speaking-dot,
    .app.listening .speaking-dot {
      display: inline-block;
    }

    @keyframes dotPulse { 50% { transform: scale(1.45); opacity: 0.65; } }

    .mic.listening {
      color: white;
      background: rgba(199,148,14,0.18);
      border-color: rgba(199,148,14,0.34);
      box-shadow: 0 0 18px rgba(199,148,14,0.22);
    }

    @media (max-width: 680px) {
      .app {
        width: 100%;
        padding-left: 14px;
        padding-right: 14px;
      }

      .topbar { justify-content: flex-start; }
      .main { gap: 20px; }
      .composer { min-height: 150px; border-radius: 26px; padding: 16px; }
      .model-label { display: none; }
      .chips { justify-content: flex-start; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 4px; }
      .chip { flex: 0 0 auto; }
      .app.has-chat .chat { max-height: 46dvh; }
    }
  </style>
</head>
<body>
  <main class="app" id="app">
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true"></div>
        <div>AyAstra</div>
      </div>
    </header>

    <section class="main">
      <section class="hero" id="hero">
        <h1 class="greeting" id="greeting">What's on your mind, Ayanda?</h1>
        <p class="quote" id="quote">Small steps, sharp focus. We build the future one clean commit at a time.</p>
      </section>

      <section class="chat" id="chat" aria-live="polite"></section>
    </section>

    <section class="composer-wrap">
      <form class="composer" id="chatForm">
        <textarea id="messageInput" rows="2" placeholder="How can I help you today?"></textarea>
        <div class="composer-actions">
          <div class="left-actions">
            <button class="icon-btn" type="button" title="New attachment coming later">＋</button>
            <button class="icon-btn mic" id="micButton" type="button" title="Voice input where supported">♬</button>
          </div>
          <div class="right-actions">
            <span class="speaking-dot"></span>
            <span class="model-label">QuantaCore</span>
            <button class="send-btn" type="submit" title="Send">↑</button>
          </div>
        </div>
      </form>

      <div class="chips" id="chips">
        <button class="chip" data-prompt="Help me write a study plan for this week"><span>✎</span> Write</button>
        <button class="chip" data-prompt="/tutor APIs"><span>🎓</span> Learn</button>
        <button class="chip" data-prompt="Explain this coding concept step by step"><span>&lt;/&gt;</span> Code</button>
        <button class="chip" data-prompt="Help me plan my day"><span>☕</span> Life stuff</button>
        <button class="chip" data-prompt="/news ai"><span>📰</span> AI updates</button>
        <button class="chip" data-prompt="/research AI agents in education"><span>🔎</span> Research</button>
      </div>

      <div class="status-line" id="statusLine">Ready when you are.</div>
    </section>
  </main>

  <script>
    const app = document.getElementById('app');
    const form = document.getElementById('chatForm');
    const input = document.getElementById('messageInput');
    const chat = document.getElementById('chat');
    const statusLine = document.getElementById('statusLine');
    const micButton = document.getElementById('micButton');
    const greeting = document.getElementById('greeting');
    const quote = document.getElementById('quote');

    const greetings = [
      "What's on your mind, Ayanda?",
      "Ready to build something brilliant?",
      "What are we solving today?",
      "Hello Ayanda. What needs your genius?",
      "What mission are we handling today?"
    ];

    const quotes = [
      "Small steps, sharp focus. We build the future one clean commit at a time.",
      "Your future self is watching. Let's give her something impressive.",
      "No chaos. We think, we build, we test, we commit.",
      "A royal lab does not run on panic. It runs on systems.",
      "Ask boldly. Verify facts. Build carefully."
    ];

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let listening = false;

    function randomItem(items) {
      return items[Math.floor(Math.random() * items.length)];
    }

    greeting.textContent = randomItem(greetings);
    quote.textContent = randomItem(quotes);

    function setState(state, text) {
      app.classList.remove('thinking', 'speaking', 'listening');
      if (state) app.classList.add(state);
      statusLine.textContent = text || 'Ready when you are.';
    }

    function addMessage(role, text) {
      app.classList.add('has-chat');
      const div = document.createElement('div');
      div.className = `message ${role}`;
      div.textContent = text;
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
    }

    function cleanForSpeech(text) {
      return String(text)
        .replace(/^AyAstra:\s*/i, '')
        .replace(/https?:\/\/\S+/g, 'link available in the response')
        .slice(0, 950);
    }

    function speak(text) {
      const clean = cleanForSpeech(text);

      if (!('speechSynthesis' in window)) {
        setState('speaking', 'Responding...');
        setTimeout(() => setState('', 'Ready when you are.'), Math.min(5200, Math.max(1200, clean.length * 20)));
        return;
      }

      speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(clean);
      utterance.rate = 0.98;
      utterance.pitch = 1.05;
      utterance.onstart = () => setState('speaking', 'Speaking...');
      utterance.onend = () => setState('', 'Ready when you are.');
      utterance.onerror = () => setState('', 'Ready when you are.');
      speechSynthesis.speak(utterance);
    }

    async function sendMessage(message) {
      const text = String(message || '').trim();
      if (!text) return;

      input.value = '';
      addMessage('user', text);
      setState('thinking', 'Thinking...');

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text }),
        });

        if (!response.ok) throw new Error(`Request failed: ${response.status}`);

        const data = await response.json();
        addMessage('assistant', data.response);
        speak(data.response);
      } catch (error) {
        const message = `AyAstra: Interface error: ${error.message}`;
        addMessage('assistant', message);
        speak(message);
      }
    }

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      sendMessage(input.value);
    });

    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage(input.value);
      }
    });

    document.querySelectorAll('.chip').forEach((chip) => {
      chip.addEventListener('click', () => sendMessage(chip.dataset.prompt));
    });

    function setupRecognition() {
      if (!SpeechRecognition) {
        micButton.title = 'Voice input is not supported in this browser yet';
        return;
      }

      recognition = new SpeechRecognition();
      recognition.lang = 'en-ZA';
      recognition.interimResults = false;
      recognition.continuous = false;

      recognition.onstart = () => {
        listening = true;
        micButton.classList.add('listening');
        setState('listening', 'Listening...');
      };

      recognition.onend = () => {
        listening = false;
        micButton.classList.remove('listening');
        if (app.classList.contains('listening')) setState('', 'Ready when you are.');
      };

      recognition.onerror = () => {
        listening = false;
        micButton.classList.remove('listening');
        addMessage('assistant', 'AyAstra: Microphone capture failed. Browser permissions are probably being dramatic.');
        setState('', 'Ready when you are.');
      };

      recognition.onresult = (event) => {
        const transcript = event.results?.[0]?.[0]?.transcript || '';
        if (transcript) sendMessage(transcript);
      };
    }

    micButton.addEventListener('click', () => {
      if (!recognition) {
        addMessage('assistant', 'AyAstra: Voice input is not supported in this browser yet. Type for now, we adapt.');
        return;
      }

      if (listening) {
        recognition.stop();
        return;
      }

      recognition.start();
    });

    setupRecognition();
    input.focus();
  </script>
</body>
</html>
'''
