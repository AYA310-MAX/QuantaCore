"""Focused multi-page LLM-style chat UI for AyAstra / QuantaCore.

This is the Sprint 12 UI direction:
- not a dashboard
- modern dark minimal chat app
- HOME, Chats, Files, Settings screens
- file/image attachment UI
- responsive mobile + desktop layout

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

from ay_astra.assistant import handle_message

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
                    "background_color": "#0F172A",
                    "theme_color": "#6366F1",
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
                self._send_json({"response": "AyAstra: Type a message first, Ayanda."})
                return

            response = handle_message(message)
            if response == "__EXIT__":
                response = "AyAstra: The chat interface stays online. Close the tab or stop the server with Ctrl+C."

            self._send_json({"response": response})
            return

        self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format: str, *args: Any) -> None:
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

    print("AyAstra Chat UI online — Sprint 12 interface active.")
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
  <meta name="theme-color" content="#0F172A" />
  <link rel="manifest" href="/manifest.json" />
  <title>AyAstra</title>

  <style>
    :root {
      --base-950: #0F172A;
      --base-900: #111827;
      --base-850: #151C2E;
      --base-800: #1F2937;
      --amethyst: #390040;
      --deep-amethyst: #1F0035;
      --violet: #5A0060;
      --royal-blue: #0C111F;
      --indigo: #6366F1;
      --indigo-hover: #4F46E5;
      --teal: #14B8A6;
      --gold: #C7940E;
      --peach: #ED9E6F;
      --plum: #80466E;
      --text: #F9FAFB;
      --text-soft: #CBD5E1;
      --text-muted: rgba(249, 250, 251, 0.56);
      --line: rgba(255, 255, 255, 0.09);
      --line-strong: rgba(255, 255, 255, 0.14);
      --panel: rgba(31, 41, 55, 0.86);
      --panel-soft: rgba(31, 41, 55, 0.62);
      --shadow-soft: 0 24px 64px rgba(0, 0, 0, 0.22);
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
        radial-gradient(circle at 12% 10%, rgba(57, 0, 64, 0.42), transparent 28%),
        radial-gradient(circle at 92% 18%, rgba(99, 102, 241, 0.20), transparent 26%),
        radial-gradient(circle at 18% 88%, rgba(20, 184, 166, 0.10), transparent 24%),
        linear-gradient(135deg, var(--base-950), var(--royal-blue) 48%, var(--base-900));
      overflow-x: hidden;
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: 0.08;
      background-image:
        linear-gradient(rgba(255,255,255,0.14) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.14) 1px, transparent 1px);
      background-size: 56px 56px;
      mask-image: linear-gradient(to bottom, black, transparent 88%);
    }

    button, input, textarea { font: inherit; }
    button { cursor: pointer; }

    .app-shell {
      position: relative;
      z-index: 1;
      min-height: 100dvh;
      display: grid;
      grid-template-columns: 240px minmax(0, 1fr);
    }

    .sidebar {
      position: sticky;
      top: 0;
      height: 100dvh;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 16px;
      padding: 20px 16px;
      border-right: 1px solid var(--line);
      background: rgba(12, 17, 31, 0.72);
      backdrop-filter: blur(20px);
    }

    .sidebar-brand,
    .top-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 40px;
    }

    .logo {
      width: 32px;
      height: 32px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      color: white;
      font-weight: 700;
      font-size: 14px;
      background: radial-gradient(circle at 32% 22%, #ffffff 0 4%, var(--teal) 9%, var(--indigo) 38%, var(--violet) 72%);
      box-shadow: 0 0 22px rgba(99, 102, 241, 0.28);
    }

    .app-name {
      font-size: 18px;
      font-weight: 650;
      letter-spacing: -0.02em;
    }

    .nav-list {
      display: grid;
      gap: 6px;
    }

    .nav-item {
      height: 42px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 12px;
      border: 1px solid transparent;
      border-radius: 12px;
      color: var(--text-soft);
      background: transparent;
      text-align: left;
      font-size: 14px;
    }

    .nav-item:hover,
    .nav-item.active {
      color: white;
      border-color: rgba(99, 102, 241, 0.18);
      background: rgba(99, 102, 241, 0.10);
    }

    .nav-item svg { width: 22px; height: 22px; stroke-width: 1.75; }

    .recent-title {
      margin: 12px 8px 8px;
      color: var(--text-muted);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .recent-list {
      display: grid;
      gap: 6px;
      overflow: hidden;
    }

    .recent-item {
      padding: 10px 12px;
      border-radius: 10px;
      color: var(--text-muted);
      background: rgba(255,255,255,0.03);
      font-size: 13px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .main-wrap {
      min-width: 0;
      min-height: 100dvh;
      display: grid;
      grid-template-rows: auto 1fr auto;
      padding: max(14px, env(safe-area-inset-top, 0px)) clamp(16px, 4vw, 32px) calc(82px + var(--safe-bottom));
    }

    .topbar {
      min-height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .top-title {
      font-size: 22px;
      font-weight: 650;
      letter-spacing: -0.02em;
    }

    .top-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .avatar {
      width: 32px;
      height: 32px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--amethyst), var(--indigo));
      color: white;
      font-size: 13px;
      font-weight: 650;
    }

    .icon-btn {
      width: 36px;
      height: 36px;
      display: grid;
      place-items: center;
      border: 0;
      border-radius: 10px;
      color: var(--text-soft);
      background: rgba(255,255,255,0.045);
      transition: background 0.16s ease, transform 0.16s ease;
    }

    .icon-btn:hover { background: rgba(255,255,255,0.075); }
    .icon-btn:active { transform: scale(0.97); }
    .icon-btn svg { width: 20px; height: 20px; stroke-width: 1.75; }

    .page {
      display: none;
      min-height: 0;
    }

    body[data-page="home"] #page-home,
    body[data-page="chats"] #page-chats,
    body[data-page="files"] #page-files,
    body[data-page="settings"] #page-settings {
      display: block;
    }

    .home-stage {
      min-height: calc(100dvh - 170px);
      display: grid;
      place-items: center;
      padding: 28px 0;
    }

    .chat-card {
      width: min(100%, 420px);
      max-width: 480px;
      display: grid;
      grid-template-rows: auto minmax(220px, 1fr) auto;
      min-height: 620px;
      max-height: calc(100dvh - 150px);
      border: 1px solid var(--line-strong);
      border-radius: 28px;
      background: var(--panel);
      box-shadow: var(--shadow-soft);
      backdrop-filter: blur(22px);
      overflow: hidden;
    }

    .chat-card-header {
      min-height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
    }

    .assistant-meta {
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }

    .assistant-avatar {
      width: 32px;
      height: 32px;
      flex: 0 0 auto;
      border-radius: 999px;
      background: radial-gradient(circle at 30% 20%, white 0 5%, var(--teal) 11%, var(--indigo) 42%, var(--violet) 80%);
    }

    .assistant-title {
      font-size: 15px;
      font-weight: 650;
    }

    .assistant-subtitle {
      margin-top: 1px;
      color: var(--text-muted);
      font-size: 12px;
    }

    .status-chip {
      height: 24px;
      display: inline-flex;
      align-items: center;
      padding: 0 10px;
      border: 1px solid rgba(20, 184, 166, 0.22);
      border-radius: 999px;
      color: var(--teal);
      background: rgba(20, 184, 166, 0.12);
      font-size: 12px;
      white-space: nowrap;
    }

    .messages {
      min-height: 0;
      display: flex;
      flex-direction: column;
      gap: 12px;
      overflow-y: auto;
      padding: 16px;
      scroll-behavior: smooth;
    }

    .messages::before {
      content: "";
      position: sticky;
      top: -16px;
      height: 12px;
      margin-bottom: -12px;
      background: linear-gradient(to bottom, rgba(31,41,55,0.95), transparent);
      pointer-events: none;
      z-index: 2;
    }

    .message-row {
      display: grid;
      gap: 4px;
    }

    .message-row.user { justify-items: end; }
    .message-row.assistant { justify-items: start; }

    .bubble {
      max-width: 80%;
      padding: 12px 14px;
      border-radius: 16px;
      line-height: 1.55;
      font-size: 14px;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .message-row.assistant .bubble {
      color: var(--text);
      border: 1px solid rgba(99, 102, 241, 0.18);
      background: rgba(255,255,255,0.055);
    }

    .message-row.user .bubble {
      color: white;
      background: var(--indigo);
    }

    .timestamp {
      color: var(--text-muted);
      font-size: 11px;
      padding: 0 4px;
    }

    .typing {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      height: 18px;
    }

    .typing span {
      width: 5px;
      height: 5px;
      border-radius: 999px;
      background: rgba(255,255,255,0.55);
      animation: typingPulse 0.9s ease-in-out infinite;
    }

    .typing span:nth-child(2) { animation-delay: 0.13s; }
    .typing span:nth-child(3) { animation-delay: 0.26s; }

    @keyframes typingPulse {
      50% { opacity: 0.35; transform: translateY(-2px); }
    }

    .image-card {
      display: grid;
      gap: 8px;
      width: min(100%, 320px);
      margin-top: 8px;
      padding: 8px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: rgba(0,0,0,0.16);
    }

    .image-card img {
      width: 100%;
      max-height: 220px;
      object-fit: cover;
      border-radius: 12px;
    }

    .image-caption {
      color: var(--text-soft);
      font-size: 13px;
    }

    .image-source {
      color: #A5B4FC;
      font-size: 12px;
      text-decoration: none;
    }

    .composer-zone {
      display: grid;
      gap: 8px;
      padding: 12px;
      border-top: 1px solid var(--line);
      background: rgba(15,23,42,0.72);
    }

    .attachment-tray {
      display: none;
      gap: 8px;
      overflow-x: auto;
      padding: 0 2px 2px;
    }

    .attachment-tray.show { display: flex; }

    .file-chip {
      width: 220px;
      height: 36px;
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 0 8px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: rgba(255,255,255,0.055);
    }

    .file-chip svg { width: 18px; height: 18px; stroke-width: 1.75; }
    .file-name {
      min-width: 0;
      flex: 1;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      color: var(--text-soft);
      font-size: 13px;
    }

    .remove-chip {
      width: 24px;
      height: 24px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      background: transparent;
      border: 0;
      color: var(--text-muted);
    }

    .thumb-strip {
      display: none;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 2px;
    }

    .thumb-strip.show { display: flex; }

    .thumb {
      position: relative;
      width: 72px;
      height: 72px;
      flex: 0 0 auto;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.04);
    }

    .thumb img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .thumb button {
      position: absolute;
      top: 4px;
      right: 4px;
      width: 22px;
      height: 22px;
      border-radius: 999px;
      border: 0;
      color: white;
      background: rgba(0,0,0,0.52);
    }

    .input-bar {
      min-height: 60px;
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 8px;
      padding: 8px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(15,23,42,0.82);
    }

    .input-icons {
      display: flex;
      gap: 4px;
      align-items: center;
    }

    .input-icon {
      width: 36px;
      height: 36px;
      display: grid;
      place-items: center;
      border: 0;
      border-radius: 10px;
      color: var(--text-soft);
      background: transparent;
    }

    .input-icon:hover { background: rgba(255,255,255,0.075); }
    .input-icon svg { width: 21px; height: 21px; stroke-width: 1.75; }

    .message-input {
      width: 100%;
      height: 42px;
      min-width: 0;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      outline: 0;
      color: var(--text);
      background: rgba(255,255,255,0.04);
      padding: 0 12px;
      font-size: 14px;
    }

    .message-input:focus {
      border-color: var(--indigo);
      box-shadow: 0 0 0 3px rgba(99,102,241,0.16);
    }

    .message-input::placeholder { color: rgba(249,250,251,0.42); }

    .send-button {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border: 0;
      border-radius: 999px;
      color: white;
      background: var(--indigo);
      transition: background 0.16s ease, transform 0.16s ease;
    }

    .send-button:hover { background: var(--indigo-hover); }
    .send-button:active { transform: scale(0.97); }
    .send-button svg { width: 21px; height: 21px; stroke-width: 1.75; }

    .prompt-chips {
      width: min(100%, 520px);
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
      margin: 16px auto 0;
    }

    .prompt-chip {
      height: 38px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 0 14px;
      border: 1px solid var(--line);
      border-radius: 12px;
      color: var(--text-soft);
      background: rgba(255,255,255,0.035);
      font-size: 14px;
    }

    .prompt-chip svg { width: 17px; height: 17px; stroke-width: 1.75; }

    .page-inner {
      width: min(100%, 960px);
      margin: 0 auto;
      padding: 24px 0 84px;
    }

    .page-header {
      display: grid;
      gap: 12px;
      margin-bottom: 18px;
    }

    .page-title {
      margin: 0;
      font-size: 26px;
      font-weight: 650;
      letter-spacing: -0.03em;
    }

    .search-input {
      height: 42px;
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 12px;
      outline: 0;
      color: var(--text);
      background: rgba(31,41,55,0.76);
      padding: 0 14px;
    }

    .list-page {
      display: grid;
      gap: 10px;
    }

    .conversation-item {
      min-height: 80px;
      display: grid;
      grid-template-columns: 36px 1fr auto;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: rgba(31,41,55,0.72);
    }

    .mini-avatar {
      width: 36px;
      height: 36px;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--indigo), var(--violet));
    }

    .conversation-title { font-size: 15px; font-weight: 650; }
    .conversation-preview { margin-top: 3px; color: var(--text-muted); font-size: 13px; }
    .conversation-time { color: var(--text-muted); font-size: 12px; }

    .filter-row {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      margin-bottom: 16px;
      padding-bottom: 2px;
    }

    .filter-chip {
      height: 30px;
      flex: 0 0 auto;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: var(--text-soft);
      background: rgba(255,255,255,0.04);
      font-size: 13px;
    }

    .filter-chip.active {
      color: #A5B4FC;
      background: rgba(99,102,241,0.14);
      border-color: rgba(99,102,241,0.20);
    }

    .file-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 14px;
    }

    .file-card {
      min-height: 146px;
      display: grid;
      gap: 12px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: rgba(31,41,55,0.72);
    }

    .file-card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }

    .file-card svg { width: 26px; height: 26px; stroke-width: 1.75; }
    .file-card-name { font-size: 14px; font-weight: 600; }
    .file-card-meta { color: var(--text-muted); font-size: 12px; }

    .file-actions {
      display: flex;
      gap: 6px;
      align-items: center;
    }

    .file-actions button {
      width: 32px;
      height: 32px;
      display: grid;
      place-items: center;
      border: 0;
      border-radius: 8px;
      color: var(--text-soft);
      background: rgba(255,255,255,0.045);
    }

    .settings-grid {
      display: grid;
      gap: 14px;
    }

    .settings-card {
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: rgba(31,41,55,0.72);
    }

    .settings-title {
      margin: 0 0 12px;
      font-size: 18px;
      font-weight: 600;
    }

    .setting-row {
      min-height: 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      border-top: 1px solid rgba(255,255,255,0.06);
      padding: 12px 0;
    }

    .setting-row:first-of-type { border-top: 0; }
    .setting-label { font-size: 14px; }
    .setting-help { margin-top: 3px; color: var(--text-muted); font-size: 12px; }

    .switch {
      width: 40px;
      height: 24px;
      border-radius: 999px;
      background: var(--indigo);
      position: relative;
    }

    .switch::after {
      content: "";
      position: absolute;
      top: 3px;
      right: 3px;
      width: 18px;
      height: 18px;
      border-radius: 999px;
      background: white;
    }

    .slider {
      width: 140px;
      height: 6px;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--indigo) 62%, rgba(255,255,255,0.12) 62%);
      position: relative;
    }

    .slider::after {
      content: "";
      position: absolute;
      left: calc(62% - 8px);
      top: -5px;
      width: 16px;
      height: 16px;
      border-radius: 999px;
      background: white;
    }

    .bottom-nav {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 20;
      height: calc(64px + var(--safe-bottom));
      display: none;
      grid-template-columns: repeat(4, 1fr);
      padding-bottom: var(--safe-bottom);
      border-top: 1px solid var(--line);
      background: rgba(17,24,39,0.94);
      backdrop-filter: blur(18px);
    }

    .bottom-tab {
      display: grid;
      place-items: center;
      align-content: center;
      gap: 4px;
      border: 0;
      background: transparent;
      color: var(--text-muted);
      font-size: 11px;
    }

    .bottom-tab svg { width: 24px; height: 24px; stroke-width: 1.75; }
    .bottom-tab.active { color: var(--indigo); }

    .empty-state {
      min-height: 220px;
      display: grid;
      place-items: center;
      text-align: center;
      color: var(--text-muted);
      border: 1px dashed var(--line-strong);
      border-radius: 18px;
      background: rgba(255,255,255,0.025);
      padding: 24px;
    }

    @media (max-width: 920px) {
      .app-shell { grid-template-columns: 1fr; }
      .sidebar { display: none; }
      .main-wrap { padding-bottom: calc(86px + var(--safe-bottom)); }
      .bottom-nav { display: grid; }
      .chat-card {
        width: calc(100vw - 32px);
        min-height: min(640px, calc(100dvh - 178px));
        max-height: calc(100dvh - 178px);
      }
      .prompt-chips {
        justify-content: flex-start;
        overflow-x: auto;
        flex-wrap: nowrap;
        padding-bottom: 2px;
      }
      .prompt-chip { flex: 0 0 auto; }
    }

    @media (max-width: 520px) {
      .top-title { font-size: 20px; }
      .chat-card {
        width: calc(100vw - 24px);
        border-radius: 24px;
      }
      .input-bar {
        grid-template-columns: 1fr auto;
      }
      .input-icons {
        grid-column: 1 / -1;
      }
      .message-input {
        height: 44px;
      }
      .bubble { max-width: 86%; }
    }
  </style>
</head>
<body data-page="home">
  <div class="app-shell">
    <aside class="sidebar" aria-label="Desktop navigation">
      <div class="sidebar-brand">
        <div class="logo">A</div>
        <div class="app-name">AyAstra</div>
      </div>

      <nav class="nav-list" id="sidebarNav"></nav>

      <div>
        <div class="recent-title">Recent chats</div>
        <div class="recent-list" id="recentList"></div>
      </div>

      <div class="status-chip">Ready to help</div>
    </aside>

    <main class="main-wrap">
      <header class="topbar">
        <div class="top-brand">
          <div class="logo">A</div>
          <div class="top-title" id="pageTitle">HOME</div>
        </div>
        <div class="top-actions">
          <button class="icon-btn" data-page-target="settings" title="Settings" aria-label="Settings"></button>
          <div class="avatar">AD</div>
        </div>
      </header>

      <section class="page" id="page-home">
        <div class="home-stage">
          <div>
            <section class="chat-card" aria-label="AyAstra chat">
              <header class="chat-card-header">
                <div class="assistant-meta">
                  <div class="assistant-avatar"></div>
                  <div>
                    <div class="assistant-title">Ask AyAstra anything</div>
                    <div class="assistant-subtitle">QuantaCore active</div>
                  </div>
                </div>
                <div class="status-chip">Online</div>
              </header>

              <div class="messages" id="messages"></div>

              <div class="composer-zone">
                <div class="attachment-tray" id="fileTray"></div>
                <div class="thumb-strip" id="imageTray"></div>

                <form class="input-bar" id="chatForm">
                  <div class="input-icons">
                    <button class="input-icon" type="button" id="fileButton" title="Attach file"></button>
                    <button class="input-icon" type="button" id="imageButton" title="Attach image"></button>
                    <button class="input-icon" type="button" id="internetImageButton" title="Add internet image"></button>
                  </div>

                  <input class="message-input" id="messageInput" autocomplete="off" placeholder="Type a message or ask a question…" />
                  <button class="send-button" type="submit" title="Send"></button>
                </form>
              </div>
            </section>

            <div class="prompt-chips" id="promptChips"></div>
          </div>
        </div>
      </section>

      <section class="page" id="page-chats">
        <div class="page-inner">
          <div class="page-header">
            <h1 class="page-title">Chats</h1>
            <input class="search-input" id="chatSearch" placeholder="Search chats…" />
          </div>
          <div class="list-page" id="chatList"></div>
        </div>
      </section>

      <section class="page" id="page-files">
        <div class="page-inner">
          <div class="page-header">
            <h1 class="page-title">Files</h1>
            <div class="filter-row" id="fileFilters"></div>
          </div>
          <div class="file-grid" id="fileGrid"></div>
        </div>
      </section>

      <section class="page" id="page-settings">
        <div class="page-inner">
          <div class="page-header">
            <h1 class="page-title">Settings</h1>
          </div>
          <div class="settings-grid" id="settingsGrid"></div>
        </div>
      </section>
    </main>
  </div>

  <nav class="bottom-nav" id="bottomNav" aria-label="Mobile navigation"></nav>

  <input type="file" id="fileInput" multiple hidden />
  <input type="file" id="imageInput" accept="image/*" multiple hidden />

  <script>
    const icons = {
      home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg>',
      chats: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z"/></svg>',
      files: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 6a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/></svg>',
      settings: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 15.5A3.5 3.5 0 1 0 12 8a3.5 3.5 0 0 0 0 7.5Z"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.6-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.6V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.1a2 2 0 1 1 0 4H21a1.7 1.7 0 0 0-1.6 1Z"/></svg>',
      paperclip: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m21.4 11.6-8.5 8.5a6 6 0 0 1-8.5-8.5l9.2-9.2a4 4 0 0 1 5.7 5.7l-9.2 9.2a2 2 0 1 1-2.8-2.8l8.5-8.5"/></svg>',
      image: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8" cy="10" r="2"/><path d="m21 15-4.5-4.5L9 18"/></svg>',
      globe: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20"/><path d="M12 2a15 15 0 0 0 0 20"/></svg>',
      send: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>',
      file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/></svg>',
      x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
      more: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>',
      open: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 3h7v7"/><path d="M10 14 21 3"/><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"/></svg>'
    };

    const state = {
      activePage: 'home',
      fileFilter: 'All',
      messages: [
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: 'AyAstra is online. Ask me something, upload a file, add an image, or request source-backed news.',
          timestamp: timeNow()
        }
      ],
      conversations: [
        { id: 'current', title: 'Current conversation', preview: 'AyAstra is ready to help.', time: 'Now' }
      ],
      attachedFiles: [],
      attachedImages: [],
      library: []
    };

    const navItems = [
      { id: 'home', label: 'Home', icon: icons.home },
      { id: 'chats', label: 'Chats', icon: icons.chats },
      { id: 'files', label: 'Files', icon: icons.files },
      { id: 'settings', label: 'Settings', icon: icons.settings }
    ];

    const prompts = [
      { label: 'Write', prompt: 'Help me write a clear study plan for this week.' },
      { label: 'Learn', prompt: '/tutor APIs' },
      { label: 'Code', prompt: 'Explain this coding concept step by step.' },
      { label: 'Life stuff', prompt: 'Help me plan my day.' },
      { label: 'AI updates', prompt: '/news ai' },
      { label: 'Research', prompt: '/research AI agents in education' }
    ];

    const filters = ['All', 'Documents', 'Images', 'PDFs', 'Sources'];

    const settingsSections = [
      {
        title: 'AI Behavior',
        rows: [
          { label: 'Source-first answers', help: 'Use verified tools for news and research.', control: 'switch' },
          { label: 'Tutor mode detail', help: 'Adjust how detailed explanations should be.', control: 'slider' }
        ]
      },
      {
        title: 'Integrations',
        rows: [
          { label: 'Calendar integration', help: 'Planned for a future sprint.', control: 'switch' },
          { label: 'Smart-home bridge', help: 'Future Home Assistant connection.', control: 'switch' }
        ]
      },
      {
        title: 'Appearance',
        rows: [
          { label: 'Dark amethyst theme', help: 'Current visual direction.', control: 'switch' },
          { label: 'Interface density', help: 'Keep spacing minimal and readable.', control: 'slider' }
        ]
      }
    ];

    const pageTitle = document.getElementById('pageTitle');
    const sidebarNav = document.getElementById('sidebarNav');
    const bottomNav = document.getElementById('bottomNav');
    const messagesEl = document.getElementById('messages');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const fileButton = document.getElementById('fileButton');
    const imageButton = document.getElementById('imageButton');
    const internetImageButton = document.getElementById('internetImageButton');
    const fileInput = document.getElementById('fileInput');
    const imageInput = document.getElementById('imageInput');
    const fileTray = document.getElementById('fileTray');
    const imageTray = document.getElementById('imageTray');
    const promptChips = document.getElementById('promptChips');
    const chatList = document.getElementById('chatList');
    const recentList = document.getElementById('recentList');
    const fileFilters = document.getElementById('fileFilters');
    const fileGrid = document.getElementById('fileGrid');
    const settingsGrid = document.getElementById('settingsGrid');

    document.querySelector('[data-page-target="settings"]').innerHTML = icons.settings;
    fileButton.innerHTML = icons.paperclip;
    imageButton.innerHTML = icons.image;
    internetImageButton.innerHTML = icons.globe;
    document.querySelector('.send-button').innerHTML = icons.send;

    function timeNow() {
      return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function escapeHtml(value) {
      return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
    }

    function formatBytes(bytes) {
      if (!bytes) return '0 B';
      const units = ['B', 'KB', 'MB', 'GB'];
      let size = bytes;
      let index = 0;
      while (size >= 1024 && index < units.length - 1) {
        size /= 1024;
        index += 1;
      }
      return `${size.toFixed(size >= 10 || index === 0 ? 0 : 1)} ${units[index]}`;
    }

    function setPage(page) {
      state.activePage = page;
      document.body.dataset.page = page;
      pageTitle.textContent = page.toUpperCase();
      renderNavigation();
      renderPages();
    }

    function renderNavigation() {
      const navHtml = navItems.map(item => `
        <button class="nav-item ${state.activePage === item.id ? 'active' : ''}" data-nav="${item.id}">
          ${item.icon}<span>${item.label}</span>
        </button>
      `).join('');

      const bottomHtml = navItems.map(item => `
        <button class="bottom-tab ${state.activePage === item.id ? 'active' : ''}" data-nav="${item.id}">
          ${item.icon}<span>${item.label}</span>
        </button>
      `).join('');

      sidebarNav.innerHTML = navHtml;
      bottomNav.innerHTML = bottomHtml;

      document.querySelectorAll('[data-nav]').forEach(button => {
        button.addEventListener('click', () => setPage(button.dataset.nav));
      });
    }

    function renderMessages() {
      messagesEl.innerHTML = state.messages.map(message => `
        <div class="message-row ${message.role}">
          <div class="bubble">
            <div>${escapeHtml(message.content)}</div>
            ${renderMessageFiles(message.files || [])}
            ${renderMessageImages(message.images || [])}
            ${renderInternetImages(message.internetImages || [])}
          </div>
          <div class="timestamp">${escapeHtml(message.timestamp || '')}</div>
        </div>
      `).join('');
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function renderMessageFiles(files) {
      if (!files.length) return '';
      return `<div style="display:grid;gap:6px;margin-top:8px;">${files.map(file => `
        <div class="file-chip" style="width:min(220px,100%);">
          ${icons.file}<span class="file-name">${escapeHtml(file.name)}</span>
        </div>
      `).join('')}</div>`;
    }

    function renderMessageImages(images) {
      if (!images.length) return '';
      return `<div class="thumb-strip show" style="margin-top:8px;">${images.map(image => `
        <div class="thumb"><img src="${image.url}" alt="${escapeHtml(image.name)}"></div>
      `).join('')}</div>`;
    }

    function renderInternetImages(images) {
      if (!images.length) return '';
      return images.map(image => `
        <div class="image-card">
          <img src="${image.url}" alt="${escapeHtml(image.caption || 'Internet image')}" loading="lazy">
          ${image.caption ? `<div class="image-caption">${escapeHtml(image.caption)}</div>` : ''}
          <a class="image-source" href="${image.url}" target="_blank" rel="noreferrer">Open source</a>
        </div>
      `).join('');
    }

    function renderAttachments() {
      fileTray.classList.toggle('show', state.attachedFiles.length > 0);
      imageTray.classList.toggle('show', state.attachedImages.length > 0);

      fileTray.innerHTML = state.attachedFiles.map(file => `
        <div class="file-chip">
          ${icons.file}
          <span class="file-name">${escapeHtml(file.name)}</span>
          <button class="remove-chip" data-remove-file="${file.id}" type="button">${icons.x}</button>
        </div>
      `).join('');

      imageTray.innerHTML = state.attachedImages.map(image => `
        <div class="thumb">
          <img src="${image.url}" alt="${escapeHtml(image.name)}">
          <button data-remove-image="${image.id}" type="button">×</button>
        </div>
      `).join('');

      document.querySelectorAll('[data-remove-file]').forEach(button => {
        button.addEventListener('click', () => {
          state.attachedFiles = state.attachedFiles.filter(file => file.id !== button.dataset.removeFile);
          renderAttachments();
        });
      });

      document.querySelectorAll('[data-remove-image]').forEach(button => {
        button.addEventListener('click', () => {
          state.attachedImages = state.attachedImages.filter(image => image.id !== button.dataset.removeImage);
          renderAttachments();
        });
      });
    }

    function renderPromptChips() {
      promptChips.innerHTML = prompts.map(prompt => `
        <button class="prompt-chip" data-prompt="${escapeHtml(prompt.prompt)}">${escapeHtml(prompt.label)}</button>
      `).join('');

      document.querySelectorAll('[data-prompt]').forEach(button => {
        button.addEventListener('click', () => sendMessage(button.dataset.prompt));
      });
    }

    function renderChats() {
      chatList.innerHTML = state.conversations.map(chat => `
        <button class="conversation-item" data-page-target="home">
          <div class="mini-avatar"></div>
          <div>
            <div class="conversation-title">${escapeHtml(chat.title)}</div>
            <div class="conversation-preview">${escapeHtml(chat.preview)}</div>
          </div>
          <div class="conversation-time">${escapeHtml(chat.time)}</div>
        </button>
      `).join('');

      recentList.innerHTML = state.conversations.slice(0, 5).map(chat => `
        <div class="recent-item">${escapeHtml(chat.title)}</div>
      `).join('');

      document.querySelectorAll('[data-page-target]').forEach(button => {
        button.addEventListener('click', () => setPage(button.dataset.pageTarget));
      });
    }

    function renderFiles() {
      fileFilters.innerHTML = filters.map(filter => `
        <button class="filter-chip ${state.fileFilter === filter ? 'active' : ''}" data-filter="${filter}">${filter}</button>
      `).join('');

      document.querySelectorAll('[data-filter]').forEach(button => {
        button.addEventListener('click', () => {
          state.fileFilter = button.dataset.filter;
          renderFiles();
        });
      });

      const filtered = state.library.filter(item => {
        if (state.fileFilter === 'All') return true;
        if (state.fileFilter === 'Documents') return item.kind === 'file';
        if (state.fileFilter === 'Images') return item.kind === 'image';
        if (state.fileFilter === 'PDFs') return item.name.toLowerCase().endsWith('.pdf');
        if (state.fileFilter === 'Sources') return item.kind === 'internet-image';
        return true;
      });

      if (!filtered.length) {
        fileGrid.innerHTML = '<div class="empty-state">No files yet. Attach a file or image from the Home screen.</div>';
        return;
      }

      fileGrid.innerHTML = filtered.map(item => `
        <article class="file-card">
          <div class="file-card-top">
            ${item.kind === 'image' || item.kind === 'internet-image' ? icons.image : icons.file}
            <div class="file-actions">
              <button title="Open">${icons.open}</button>
              <button title="More">${icons.more}</button>
            </div>
          </div>
          <div>
            <div class="file-card-name">${escapeHtml(item.name)}</div>
            <div class="file-card-meta">${escapeHtml(item.meta || item.kind)}</div>
          </div>
        </article>
      `).join('');
    }

    function renderSettings() {
      settingsGrid.innerHTML = settingsSections.map(section => `
        <section class="settings-card">
          <h2 class="settings-title">${section.title}</h2>
          ${section.rows.map(row => `
            <div class="setting-row">
              <div>
                <div class="setting-label">${row.label}</div>
                <div class="setting-help">${row.help}</div>
              </div>
              ${row.control === 'switch' ? '<div class="switch"></div>' : '<div class="slider"></div>'}
            </div>
          `).join('')}
        </section>
      `).join('');
    }

    function renderPages() {
      renderMessages();
      renderAttachments();
      renderPromptChips();
      renderChats();
      renderFiles();
      renderSettings();
    }

    function addTyping() {
      const typingId = crypto.randomUUID();
      state.messages.push({
        id: typingId,
        role: 'assistant',
        content: '',
        timestamp: '',
        typing: true
      });
      messagesEl.insertAdjacentHTML('beforeend', `
        <div class="message-row assistant" id="${typingId}">
          <div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>
        </div>
      `);
      messagesEl.scrollTop = messagesEl.scrollHeight;
      return typingId;
    }

    function removeTyping(id) {
      document.getElementById(id)?.remove();
      state.messages = state.messages.filter(message => message.id !== id);
    }

    async function sendMessage(messageText) {
      const text = String(messageText || '').trim();
      const hasAttachments = state.attachedFiles.length > 0 || state.attachedImages.length > 0;

      if (!text && !hasAttachments) return;

      const userFiles = [...state.attachedFiles];
      const userImages = [...state.attachedImages];

      state.messages.push({
        id: crypto.randomUUID(),
        role: 'user',
        content: text || 'Attached files for review.',
        timestamp: timeNow(),
        files: userFiles,
        images: userImages
      });

      state.conversations[0].preview = text || 'Attached files for review.';
      state.conversations[0].time = 'Now';

      state.attachedFiles = [];
      state.attachedImages = [];
      messageInput.value = '';
      renderPages();

      const typingId = addTyping();

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text || 'I attached files. Please acknowledge them.' })
        });

        if (!response.ok) throw new Error(`Request failed: ${response.status}`);

        const data = await response.json();
        removeTyping(typingId);

        state.messages.push({
          id: crypto.randomUUID(),
          role: 'assistant',
          content: data.response,
          timestamp: timeNow()
        });

        state.conversations[0].preview = data.response.replace(/^AyAstra:\s*/i, '').slice(0, 80);
        renderPages();
      } catch (error) {
        removeTyping(typingId);
        state.messages.push({
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `AyAstra: Interface error: ${error.message}`,
          timestamp: timeNow()
        });
        renderPages();
      }
    }

    chatForm.addEventListener('submit', event => {
      event.preventDefault();
      sendMessage(messageInput.value);
    });

    messageInput.addEventListener('keydown', event => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage(messageInput.value);
      }
    });

    fileButton.addEventListener('click', () => fileInput.click());
    imageButton.addEventListener('click', () => imageInput.click());

    fileInput.addEventListener('change', event => {
      const files = Array.from(event.target.files || []);
      files.forEach(file => {
        const item = {
          id: crypto.randomUUID(),
          kind: 'file',
          name: file.name,
          meta: `${file.type || 'file'} • ${formatBytes(file.size)}`,
          size: file.size,
          type: file.type
        };
        state.attachedFiles.push(item);
        state.library.unshift(item);
      });
      fileInput.value = '';
      renderPages();
    });

    imageInput.addEventListener('change', event => {
      const files = Array.from(event.target.files || []);
      files.forEach(file => {
        const url = URL.createObjectURL(file);
        const item = {
          id: crypto.randomUUID(),
          kind: 'image',
          name: file.name,
          meta: `${file.type || 'image'} • ${formatBytes(file.size)}`,
          size: file.size,
          type: file.type,
          url
        };
        state.attachedImages.push(item);
        state.library.unshift(item);
      });
      imageInput.value = '';
      renderPages();
    });

    internetImageButton.addEventListener('click', () => {
      const url = prompt('Paste an image URL');
      if (!url) return;
      const caption = prompt('Optional caption') || 'Internet image source';
      const item = {
        id: crypto.randomUUID(),
        kind: 'internet-image',
        name: caption,
        meta: 'Internet image source',
        url,
        caption
      };
      state.library.unshift(item);
      state.messages.push({
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'Image source added for visual reference.',
        timestamp: timeNow(),
        internetImages: [item]
      });
      renderPages();
    });

    setPage('home');
  </script>
</body>
</html>
'''
