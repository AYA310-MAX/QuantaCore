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

    .home-content {
      width: min(100%, 480px);
      display: grid;
      justify-items: center;
      gap: 16px;
    }

    .quanta-orb {
      position: relative;
      width: 154px;
      height: 154px;
      display: grid;
      place-items: center;
      margin: 0 auto 2px;
      filter: drop-shadow(0 0 30px rgba(99, 102, 241, 0.34));
    }

    .quanta-orb::before,
    .quanta-orb::after {
      content: "";
      position: absolute;
      border-radius: 999px;
      pointer-events: none;
    }

    .quanta-orb::before {
      inset: 8px;
      background: conic-gradient(
        from 30deg,
        rgba(103,232,249,0.08),
        rgba(99,102,241,0.75),
        rgba(90,0,96,0.72),
        rgba(20,184,166,0.78),
        rgba(103,232,249,0.08)
      );
      filter: blur(12px);
      opacity: 0.72;
      animation: orbRingSpin 5.6s linear infinite;
    }

    .quanta-orb::after {
      inset: 22px;
      border: 1px solid rgba(255,255,255,0.08);
      background: radial-gradient(circle, rgba(99,102,241,0.14), transparent 62%);
      box-shadow: inset 0 0 38px rgba(99,102,241,0.12);
    }

    .quanta-core {
      position: relative;
      z-index: 2;
      width: 92px;
      height: 92px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.10);
      background:
        radial-gradient(circle at 50% 42%, rgba(31,41,55,0.82), rgba(12,17,31,0.96) 62%, rgba(3,7,18,0.98)),
        linear-gradient(135deg, rgba(99,102,241,0.20), rgba(90,0,96,0.20));
      box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.10),
        inset 0 -18px 36px rgba(0,0,0,0.28),
        0 0 28px rgba(99,102,241,0.28),
        0 0 80px rgba(20,184,166,0.10);
      animation: orbIdle 4.8s ease-in-out infinite;
    }

    .quanta-core::before {
      content: "";
      position: absolute;
      inset: -18px;
      border-radius: inherit;
      background: conic-gradient(
        from 0deg,
        transparent 0 16%,
        rgba(103,232,249,0.95) 21%,
        rgba(99,102,241,0.95) 30%,
        transparent 38% 55%,
        rgba(90,0,96,0.88) 63%,
        rgba(20,184,166,0.78) 72%,
        transparent 82% 100%
      );
      filter: blur(2px);
      opacity: 0.86;
      animation: orbRingSpin 3.2s linear infinite;
      -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 9px), #000 calc(100% - 8px));
      mask: radial-gradient(farthest-side, transparent calc(100% - 9px), #000 calc(100% - 8px));
    }

    .quanta-core::after {
      content: "";
      position: absolute;
      inset: -30px;
      border-radius: inherit;
      border: 1px solid rgba(99,102,241,0.18);
      opacity: 0.28;
      transform: scale(0.86);
    }

    .orb-mic {
      position: relative;
      z-index: 3;
      width: 38px;
      height: 38px;
      color: rgba(249,250,251,0.94);
      stroke-width: 1.9;
      filter: drop-shadow(0 0 10px rgba(255,255,255,0.18));
      transition: transform 0.18s ease, color 0.18s ease;
    }

    .orb-wave {
      position: absolute;
      inset: 41px;
      border-radius: 999px;
      border: 1px solid rgba(99,102,241,0.28);
      opacity: 0;
      pointer-events: none;
    }

    body.ai-thinking .quanta-core {
      animation: orbThinking 1.1s ease-in-out infinite;
    }

    body.ai-speaking .quanta-core {
      animation: orbSpeaking 0.82s ease-in-out infinite;
    }

    body.ai-thinking .quanta-core::before,
    body.ai-speaking .quanta-core::before {
      animation-duration: 1.35s;
      opacity: 1;
    }

    body.ai-thinking .orb-mic,
    body.ai-speaking .orb-mic {
      color: white;
      transform: scale(1.04);
    }

    body.ai-thinking .orb-wave,
    body.ai-speaking .orb-wave {
      animation: orbWave 1.28s ease-out infinite;
    }

    body.ai-thinking .orb-wave:nth-child(2),
    body.ai-speaking .orb-wave:nth-child(2) {
      animation-delay: 0.2s;
      border-color: rgba(20,184,166,0.36);
    }

    body.ai-thinking .orb-wave:nth-child(3),
    body.ai-speaking .orb-wave:nth-child(3) {
      animation-delay: 0.4s;
      border-color: rgba(90,0,96,0.34);
    }

    @keyframes orbRingSpin { to { transform: rotate(360deg); } }
    @keyframes orbIdle { 50% { transform: translateY(-4px) scale(1.015); } }
    @keyframes orbThinking { 50% { transform: scale(1.035); box-shadow: inset 0 1px 0 rgba(255,255,255,0.12), inset 0 -18px 36px rgba(0,0,0,0.28), 0 0 38px rgba(99,102,241,0.38), 0 0 88px rgba(20,184,166,0.14); } }
    @keyframes orbSpeaking { 0%,100% { transform: scale(1); } 35% { transform: scale(1.065); } 70% { transform: scale(0.985); } }
    @keyframes orbWave { 0% { opacity: 0.72; transform: scale(0.72); } 100% { opacity: 0; transform: scale(1.9); } }

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
      background:
        radial-gradient(circle at 35% 24%, white 0 6%, rgba(199,210,254,0.8) 10%, transparent 20%),
        conic-gradient(from 130deg, var(--teal), var(--indigo), var(--violet), var(--gold), var(--teal));
      box-shadow: 0 0 16px rgba(99,102,241,0.45);
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
      .quanta-orb {
        width: 124px;
        height: 124px;
      }

      .quanta-core {
        width: 76px;
        height: 76px;
      }

      .orb-mic {
        width: 31px;
        height: 31px;
      }

      .orb-wave {
        inset: 34px;
      }

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


    /* Sprint 12 refinement: Echo Mind-inspired mobile-first visual language.
       This keeps AyAstra minimal, purple, glassy, and app-like without returning to a dashboard. */
    body {
      background:
        radial-gradient(circle at 50% -4%, rgba(139, 92, 246, 0.28), transparent 32%),
        radial-gradient(circle at 18% 14%, rgba(90, 0, 96, 0.48), transparent 30%),
        radial-gradient(circle at 82% 18%, rgba(99, 102, 241, 0.22), transparent 28%),
        radial-gradient(circle at 50% 105%, rgba(20, 184, 166, 0.12), transparent 28%),
        linear-gradient(135deg, #080511 0%, #140720 48%, #090A18 100%);
    }

    body::before {
      opacity: 0.18;
      background:
        radial-gradient(circle at 20% 20%, rgba(255,255,255,0.08) 0 1px, transparent 1.4px),
        radial-gradient(circle at 80% 30%, rgba(236,92,255,0.12) 0 1px, transparent 1.6px),
        radial-gradient(circle at 50% 85%, rgba(99,102,241,0.13) 0 1px, transparent 1.6px);
      background-size: 110px 110px, 180px 180px, 240px 240px;
    }

    .app-shell {
      grid-template-columns: 1fr;
    }

    .sidebar {
      display: none;
    }

    .main-wrap {
      width: min(100%, 1240px);
      margin: 0 auto;
      padding-bottom: calc(92px + var(--safe-bottom));
    }

    .topbar {
      width: min(100%, 520px);
      margin: 0 auto;
    }

    .top-title {
      font-size: 21px;
      letter-spacing: -0.025em;
    }

    .home-stage {
      min-height: calc(100dvh - 178px);
      align-items: center;
      padding: 20px 0 26px;
    }

    .home-content {
      width: min(100%, 430px);
      gap: 14px;
    }

    .quanta-orb {
      width: 132px;
      height: 132px;
      margin-bottom: -2px;
      filter: drop-shadow(0 0 26px rgba(139, 92, 246, 0.42));
    }

    .quanta-orb::before {
      inset: 10px;
      background: conic-gradient(
        from 20deg,
        rgba(103,232,249,0.04),
        rgba(139,92,246,0.88),
        rgba(236,92,255,0.58),
        rgba(20,184,166,0.56),
        rgba(103,232,249,0.04)
      );
      filter: blur(10px);
      opacity: 0.64;
    }

    .quanta-core {
      width: 82px;
      height: 82px;
      background:
        radial-gradient(circle at 50% 42%, rgba(31, 41, 55, 0.76), rgba(12, 17, 31, 0.96) 63%, rgba(3, 7, 18, 0.98)),
        linear-gradient(135deg, rgba(99,102,241,0.16), rgba(90,0,96,0.18));
      box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.10),
        inset 0 -16px 32px rgba(0,0,0,0.30),
        0 0 28px rgba(139,92,246,0.32),
        0 0 70px rgba(20,184,166,0.08);
    }

    .orb-mic {
      width: 33px;
      height: 33px;
    }

    .orb-wave {
      inset: 36px;
    }

    .chat-card {
      width: min(100%, 420px);
      min-height: min(690px, calc(100dvh - 190px));
      max-height: calc(100dvh - 190px);
      border-radius: 32px;
      border-color: rgba(255,255,255,0.18);
      background:
        linear-gradient(180deg, rgba(58, 27, 86, 0.78), rgba(18, 10, 34, 0.88) 46%, rgba(9, 10, 24, 0.92)),
        rgba(31, 41, 55, 0.84);
      box-shadow:
        0 28px 80px rgba(0,0,0,0.34),
        0 0 70px rgba(90,0,96,0.28),
        inset 0 1px 0 rgba(255,255,255,0.12);
    }

    .chat-card-header {
      border-bottom: 0;
      padding: 17px 18px 10px;
    }

    .assistant-avatar {
      width: 34px;
      height: 34px;
      background:
        radial-gradient(circle at 36% 24%, white 0 5%, rgba(199,210,254,0.85) 9%, transparent 20%),
        conic-gradient(from 140deg, var(--teal), #8B5CF6, var(--violet), var(--gold), var(--teal));
    }

    .assistant-title {
      font-size: 14px;
    }

    .assistant-subtitle {
      font-size: 12px;
    }

    .status-chip {
      height: 23px;
      font-size: 12px;
      background: rgba(20,184,166,0.10);
      border-color: rgba(20,184,166,0.18);
    }

    .assistant-shortcuts {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 8px 18px 12px;
    }

    .shortcut-card {
      min-height: 104px;
      display: grid;
      place-items: center;
      align-content: center;
      gap: 10px;
      padding: 14px 10px;
      border: 1px solid rgba(255,255,255,0.10);
      border-radius: 20px;
      color: rgba(249,250,251,0.88);
      background: rgba(255,255,255,0.055);
      text-align: center;
      font-size: 12px;
      line-height: 1.25;
    }

    .shortcut-card:hover {
      background: rgba(255,255,255,0.08);
      transform: translateY(-1px);
    }

    .shortcut-icon {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      color: rgba(249,250,251,0.86);
    }

    .shortcut-icon svg {
      width: 24px;
      height: 24px;
      stroke-width: 1.75;
    }

    .topic-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      padding: 0 18px 13px;
    }

    .topic-strip button {
      height: 34px;
      border: 1px solid rgba(255,255,255,0.09);
      border-radius: 12px;
      color: rgba(249,250,251,0.72);
      background: rgba(255,255,255,0.04);
      font-size: 12px;
    }

    .messages {
      padding: 14px 18px;
    }

    .message-row.assistant .bubble {
      background: rgba(255,255,255,0.065);
      border-color: rgba(139,92,246,0.18);
    }

    .message-row.user .bubble {
      background: linear-gradient(135deg, #7C3AED, #6366F1);
    }

    .composer-zone {
      padding: 12px 14px 14px;
      background: linear-gradient(180deg, transparent, rgba(8, 5, 17, 0.64));
      border-top: 0;
    }

    .input-bar {
      min-height: 60px;
      border-radius: 22px;
      background: rgba(255,255,255,0.07);
      border-color: rgba(255,255,255,0.12);
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.10);
    }

    .message-input {
      background: rgba(10, 9, 22, 0.44);
      border-color: rgba(255,255,255,0.08);
      border-radius: 14px;
    }

    .send-button {
      background: linear-gradient(135deg, #8B5CF6, #6366F1);
      box-shadow: 0 8px 24px rgba(99,102,241,0.26);
    }

    .prompt-chips {
      width: min(100%, 420px);
      margin-top: 14px;
    }

    .prompt-chip {
      height: 36px;
      border-radius: 13px;
      background: rgba(255,255,255,0.045);
      border-color: rgba(255,255,255,0.10);
    }

    .bottom-nav {
      display: grid;
      left: 50%;
      right: auto;
      width: min(calc(100% - 28px), 420px);
      transform: translateX(-50%);
      bottom: 12px;
      height: calc(62px + var(--safe-bottom));
      border: 1px solid rgba(255,255,255,0.13);
      border-radius: 22px;
      background: rgba(17, 12, 32, 0.82);
      box-shadow: 0 18px 60px rgba(0,0,0,0.32);
    }

    .bottom-tab.active {
      color: #A78BFA;
    }

    .page-inner {
      width: min(100%, 860px);
    }

    .conversation-item,
    .file-card,
    .settings-card {
      background: rgba(31, 20, 52, 0.72);
      border-color: rgba(255,255,255,0.10);
      box-shadow: 0 18px 44px rgba(0,0,0,0.16);
    }

    @media (min-width: 921px) {
      .bottom-nav {
        display: grid;
      }
    }

    @media (max-width: 520px) {
      .home-content {
        width: 100%;
      }

      .quanta-orb {
        width: 112px;
        height: 112px;
      }

      .quanta-core {
        width: 70px;
        height: 70px;
      }

      .orb-mic {
        width: 28px;
        height: 28px;
      }

      .orb-wave {
        inset: 31px;
      }

      .assistant-shortcuts {
        gap: 10px;
        padding-left: 14px;
        padding-right: 14px;
      }

      .shortcut-card {
        min-height: 92px;
      }

      .topic-strip {
        padding-left: 14px;
        padding-right: 14px;
      }
    }



    /* Sprint 12 refinement: cute AyAstra bubble core.
       Inspired by the supplied character-like orb references, but built as an original CSS visual. */
    .quanta-orb {
      width: 156px;
      height: 156px;
      filter: drop-shadow(0 0 34px rgba(139, 92, 246, 0.44));
    }

    .quanta-orb::before {
      inset: -2px;
      border: 0;
      background:
        radial-gradient(circle at 50% 50%, rgba(99,102,241,0.18), transparent 58%),
        conic-gradient(from 130deg, rgba(103,232,249,0.04), rgba(139,92,246,0.34), rgba(236,92,255,0.26), rgba(20,184,166,0.22), rgba(103,232,249,0.04));
      filter: blur(16px);
      opacity: 0.72;
      animation: cuteHaloSpin 8s linear infinite;
      transform: none;
    }

    .quanta-orb::after {
      inset: 8px;
      border: 1px solid rgba(255,255,255,0.07);
      background:
        radial-gradient(circle at 42% 28%, rgba(255,255,255,0.12), transparent 20%),
        radial-gradient(circle at 50% 55%, rgba(99,102,241,0.12), transparent 64%);
      box-shadow:
        inset 0 0 34px rgba(255,255,255,0.035),
        0 0 46px rgba(99,102,241,0.14);
      transform: none;
      animation: cuteOuterBreathe 5.4s ease-in-out infinite;
    }

    .quanta-core {
      width: 108px;
      height: 108px;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,0.11);
      background:
        radial-gradient(circle at 32% 22%, rgba(255,255,255,0.26), transparent 18%),
        radial-gradient(circle at 62% 62%, rgba(236,92,255,0.46), transparent 42%),
        radial-gradient(circle at 45% 72%, rgba(20,184,166,0.30), transparent 46%),
        linear-gradient(180deg, rgba(139,92,246,0.72), rgba(49,46,129,0.92) 52%, rgba(15,23,42,0.98));
      box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.18),
        inset 0 -22px 34px rgba(12,17,31,0.35),
        0 0 28px rgba(139,92,246,0.48),
        0 0 88px rgba(236,92,255,0.20);
      animation: cuteOrbIdle 4.8s ease-in-out infinite;
    }

    .quanta-core::before {
      content: "";
      position: absolute;
      inset: -24px;
      border-radius: inherit;
      background:
        radial-gradient(ellipse at 46% 42%, rgba(103,232,249,0.50), transparent 34%),
        radial-gradient(ellipse at 58% 52%, rgba(236,92,255,0.48), transparent 38%),
        radial-gradient(ellipse at 46% 70%, rgba(20,184,166,0.34), transparent 40%);
      filter: blur(16px);
      opacity: 0.72;
      mix-blend-mode: screen;
      animation: cuteAuraShift 5.8s ease-in-out infinite alternate;
      -webkit-mask: none;
      mask: none;
    }

    .quanta-core::after {
      content: "";
      position: absolute;
      inset: 1px;
      border-radius: inherit;
      background:
        radial-gradient(circle at 32% 18%, rgba(255,255,255,0.18), transparent 17%),
        linear-gradient(180deg, rgba(255,255,255,0.10), transparent 42%);
      border: 1px solid rgba(255,255,255,0.06);
      opacity: 1;
    }

    .orb-face {
      position: absolute;
      z-index: 5;
      left: 50%;
      top: 48%;
      width: 74px;
      height: 46px;
      transform: translate(-50%, -50%);
      border-radius: 999px;
      background:
        radial-gradient(ellipse at 48% 44%, rgba(103,232,249,0.52), rgba(236,92,255,0.34) 58%, rgba(15,23,42,0.08) 80%);
      box-shadow:
        0 0 22px rgba(103,232,249,0.20),
        inset 0 1px 0 rgba(255,255,255,0.09);
      animation: faceFloat 5s ease-in-out infinite;
    }

    .orb-eye {
      position: absolute;
      top: 12px;
      width: 8px;
      height: 22px;
      border-radius: 999px;
      background: rgba(255,255,255,0.95);
      box-shadow:
        0 0 10px rgba(255,255,255,0.42),
        0 0 16px rgba(103,232,249,0.26);
      animation: cuteBlink 5.6s ease-in-out infinite;
    }

    .orb-eye-left { left: 23px; }
    .orb-eye-right { right: 23px; }

    .orb-smile {
      position: absolute;
      left: 50%;
      bottom: 8px;
      width: 18px;
      height: 8px;
      transform: translateX(-50%);
      border-bottom: 2px solid rgba(255,255,255,0.55);
      border-radius: 0 0 999px 999px;
      opacity: 0.36;
    }

    .orb-blush {
      position: absolute;
      top: 25px;
      width: 14px;
      height: 7px;
      border-radius: 999px;
      background: rgba(236,92,255,0.20);
      filter: blur(3px);
      opacity: 0.42;
    }

    .orb-blush-left { left: 10px; }
    .orb-blush-right { right: 10px; }

    .orb-particles {
      position: absolute;
      inset: 0;
      z-index: 4;
      pointer-events: none;
    }

    .orb-particles span {
      position: absolute;
      width: 3px;
      height: 3px;
      border-radius: 999px;
      background: rgba(236,92,255,0.72);
      box-shadow: 0 0 10px rgba(236,92,255,0.52);
      opacity: 0;
    }

    .orb-particles span:nth-child(1) { left: 40%; top: 16%; }
    .orb-particles span:nth-child(2) { left: 52%; top: 11%; background: rgba(103,232,249,0.72); }
    .orb-particles span:nth-child(3) { left: 61%; top: 20%; }
    .orb-particles span:nth-child(4) { left: 35%; top: 24%; background: rgba(20,184,166,0.70); }
    .orb-particles span:nth-child(5) { left: 56%; top: 28%; }
    .orb-particles span:nth-child(6) { left: 47%; top: 19%; background: rgba(199,148,14,0.68); }

    body.ai-thinking .quanta-core,
    body.ai-speaking .quanta-core {
      animation: cuteOrbSpeak 1.05s ease-in-out infinite;
    }

    body.ai-thinking .orb-face,
    body.ai-speaking .orb-face {
      animation: cuteFaceTalk 0.9s ease-in-out infinite;
    }

    body.ai-thinking .orb-eye,
    body.ai-speaking .orb-eye {
      animation: cuteEyeTalk 1.1s ease-in-out infinite;
    }

    body.ai-thinking .orb-smile,
    body.ai-speaking .orb-smile {
      opacity: 0.76;
      animation: cuteMouthTalk 0.72s ease-in-out infinite;
    }

    body.ai-thinking .orb-particles span,
    body.ai-speaking .orb-particles span {
      animation: cuteParticles 1.65s ease-out infinite;
    }

    body.ai-thinking .orb-particles span:nth-child(2),
    body.ai-speaking .orb-particles span:nth-child(2) { animation-delay: 0.16s; }
    body.ai-thinking .orb-particles span:nth-child(3),
    body.ai-speaking .orb-particles span:nth-child(3) { animation-delay: 0.32s; }
    body.ai-thinking .orb-particles span:nth-child(4),
    body.ai-speaking .orb-particles span:nth-child(4) { animation-delay: 0.48s; }
    body.ai-thinking .orb-particles span:nth-child(5),
    body.ai-speaking .orb-particles span:nth-child(5) { animation-delay: 0.64s; }
    body.ai-thinking .orb-particles span:nth-child(6),
    body.ai-speaking .orb-particles span:nth-child(6) { animation-delay: 0.80s; }

    @keyframes cuteHaloSpin { to { transform: rotate(360deg); } }
    @keyframes cuteOuterBreathe { 50% { transform: scale(1.035); opacity: 0.92; } }
    @keyframes cuteOrbIdle { 50% { transform: translateY(-5px) scale(1.02); } }
    @keyframes cuteAuraShift { to { transform: translate3d(5px, -4px, 0) rotate(12deg); filter: blur(18px) hue-rotate(22deg); } }
    @keyframes faceFloat { 50% { transform: translate(-50%, calc(-50% - 2px)); } }
    @keyframes cuteBlink { 0%, 92%, 100% { transform: scaleY(1); } 95% { transform: scaleY(0.16); } }
    @keyframes cuteOrbSpeak { 0%,100% { transform: scale(1); } 50% { transform: scale(1.045); } }
    @keyframes cuteFaceTalk { 0%,100% { transform: translate(-50%, -50%) scale(1); } 50% { transform: translate(-50%, calc(-50% - 2px)) scale(1.03); } }
    @keyframes cuteEyeTalk { 0%,100% { height: 22px; } 50% { height: 18px; transform: translateY(2px); } }
    @keyframes cuteMouthTalk { 0%,100% { width: 16px; height: 7px; } 50% { width: 24px; height: 10px; } }
    @keyframes cuteParticles { 0% { opacity: 0; transform: translateY(0) scale(0.7); } 25% { opacity: 0.85; } 100% { opacity: 0; transform: translateY(-34px) scale(1.25); } }

    @media (max-width: 520px) {
      .quanta-orb {
        width: 128px;
        height: 128px;
      }

      .quanta-core {
        width: 88px;
        height: 88px;
      }

      .orb-face {
        width: 62px;
        height: 39px;
      }

      .orb-eye {
        top: 10px;
        height: 19px;
      }

      .orb-eye-left { left: 19px; }
      .orb-eye-right { right: 19px; }
    }



    /* Sprint 12 refinement: Workly-inspired desktop sidebar.
       Left navigation is calm, dark, rounded, and premium. Mobile keeps bottom nav. */
    @media (min-width: 921px) {
      .app-shell {
        grid-template-columns: 320px minmax(0, 1fr);
        gap: 0;
        padding: 24px 0 24px 24px;
      }

      .workly-sidebar {
        position: sticky;
        top: 24px;
        display: grid;
        grid-template-rows: auto auto auto auto 1fr auto auto;
        height: calc(100dvh - 48px);
        margin: 0;
        padding: 22px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 28px;
        background:
          linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.012)),
          rgba(12, 13, 18, 0.92);
        box-shadow:
          0 30px 80px rgba(0,0,0,0.34),
          inset 0 1px 0 rgba(255,255,255,0.08);
        backdrop-filter: blur(22px);
        overflow: hidden;
      }

      .workly-sidebar::before {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background:
          radial-gradient(circle at 96% 34%, rgba(99,102,241,0.16), transparent 19%),
          radial-gradient(circle at 0% 100%, rgba(90,0,96,0.14), transparent 24%);
      }

      .workly-top,
      .workly-search,
      .workly-nav,
      .workly-other,
      .boost-card,
      .user-card {
        position: relative;
        z-index: 1;
      }

      .workly-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
      }

      .workly-brand {
        min-height: 38px;
      }

      .workly-brand .logo {
        width: 34px;
        height: 34px;
        box-shadow: 0 0 24px rgba(99,102,241,0.32);
      }

      .workly-caption {
        margin-top: 1px;
        color: rgba(249,250,251,0.46);
        font-size: 12px;
      }

      .workly-collapse,
      .user-menu {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 10px;
        color: rgba(249,250,251,0.62);
        background: rgba(255,255,255,0.035);
      }

      .workly-collapse svg,
      .user-menu svg {
        width: 18px;
        height: 18px;
        stroke-width: 1.8;
      }

      .workly-search {
        height: 42px;
        display: grid;
        grid-template-columns: 20px 1fr auto;
        align-items: center;
        gap: 10px;
        margin: 22px 0 14px;
        padding: 0 11px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
        color: rgba(249,250,251,0.44);
        background: rgba(255,255,255,0.035);
      }

      .workly-search svg {
        width: 18px;
        height: 18px;
        stroke-width: 1.75;
      }

      .workly-search input {
        min-width: 0;
        width: 100%;
        height: 100%;
        border: 0;
        outline: 0;
        color: var(--text);
        background: transparent;
        font-size: 13px;
      }

      .workly-search input::placeholder {
        color: rgba(249,250,251,0.42);
      }

      .workly-search span {
        min-width: 24px;
        height: 24px;
        display: grid;
        place-items: center;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 7px;
        color: rgba(249,250,251,0.45);
        font-size: 12px;
      }

      .workly-nav {
        gap: 8px;
      }

      .workly-nav .nav-item {
        height: 42px;
        padding: 0 12px;
        border-radius: 12px;
        color: rgba(249,250,251,0.58);
        font-size: 14px;
      }

      .workly-nav .nav-item svg {
        width: 21px;
        height: 21px;
      }

      .workly-nav .nav-item:hover {
        color: rgba(249,250,251,0.88);
        background: rgba(255,255,255,0.045);
      }

      .workly-nav .nav-item.active {
        color: white;
        border-color: rgba(255,255,255,0.10);
        background:
          linear-gradient(90deg, rgba(255,255,255,0.10), rgba(99,102,241,0.24) 72%, rgba(99,102,241,0.55)),
          rgba(255,255,255,0.055);
        box-shadow:
          12px 0 28px rgba(99,102,241,0.22),
          inset 0 1px 0 rgba(255,255,255,0.08);
      }

      .workly-other {
        margin-top: 22px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.08);
      }

      .workly-other .recent-title {
        margin: 0 0 10px;
        color: rgba(249,250,251,0.42);
      }

      .workly-other-item {
        width: 100%;
        height: 38px;
        display: flex;
        align-items: center;
        padding: 0 12px;
        border: 0;
        border-radius: 10px;
        color: rgba(249,250,251,0.50);
        background: transparent;
        text-align: left;
        font-size: 13px;
      }

      .workly-other-item:hover {
        color: rgba(249,250,251,0.82);
        background: rgba(255,255,255,0.04);
      }

      .workly-spacer {
        min-height: 18px;
      }

      .boost-card {
        display: grid;
        gap: 10px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        background:
          radial-gradient(circle at 85% 100%, rgba(99,102,241,0.22), transparent 42%),
          rgba(255,255,255,0.035);
      }

      .boost-title {
        color: white;
        font-size: 15px;
        font-weight: 650;
      }

      .boost-text {
        color: rgba(249,250,251,0.50);
        font-size: 12px;
        line-height: 1.45;
      }

      .boost-button {
        height: 40px;
        border: 0;
        border-radius: 11px;
        color: white;
        background: linear-gradient(135deg, #7C3AED, #4F46E5);
        box-shadow: 0 12px 26px rgba(99,102,241,0.28);
        font-weight: 620;
      }

      .user-card {
        min-height: 58px;
        display: grid;
        grid-template-columns: 40px 1fr 34px;
        align-items: center;
        gap: 10px;
        margin-top: 14px;
        padding: 9px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        background: rgba(255,255,255,0.035);
      }

      .user-avatar-small {
        width: 40px;
        height: 40px;
        display: grid;
        place-items: center;
        border-radius: 999px;
        color: white;
        font-size: 13px;
        font-weight: 700;
        background: radial-gradient(circle at 32% 24%, rgba(255,255,255,0.95) 0 5%, #8B5CF6 18%, #390040 74%);
      }

      .user-copy {
        min-width: 0;
        color: rgba(249,250,251,0.88);
        font-size: 13px;
        font-weight: 600;
      }

      .user-copy span {
        display: block;
        margin-top: 2px;
        overflow: hidden;
        color: rgba(249,250,251,0.42);
        font-size: 12px;
        font-weight: 400;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .main-wrap {
        width: min(100%, 1120px);
        margin: 0 auto;
        padding: 18px 28px 34px;
      }

      .topbar {
        width: min(100%, 880px);
      }

      .bottom-nav {
        display: none;
      }
    }

    @media (max-width: 920px) {
      .app-shell {
        grid-template-columns: 1fr;
        padding: 0;
      }

      .sidebar {
        display: none;
      }

      .bottom-nav {
        display: grid;
      }
    }



    /* Sprint 12 refinement: responsive left sidebar drawer.
       The navigation is called Sidebar on all devices. On phones it opens from the left and can be closed. */
    .sidebar-open-button {
      display: none;
      flex: 0 0 auto;
    }

    .sidebar-backdrop {
      display: none;
    }

    @media (max-width: 920px) {
      .app-shell {
        grid-template-columns: 1fr;
        padding: 0;
      }

      .sidebar-open-button {
        display: grid;
      }

      .topbar {
        width: 100%;
        justify-content: flex-start;
      }

      .top-brand {
        flex: 1;
      }

      .sidebar-backdrop {
        position: fixed;
        inset: 0;
        z-index: 39;
        display: block;
        background: rgba(0, 0, 0, 0.54);
        opacity: 0;
        pointer-events: none;
        transition: opacity 180ms ease;
        backdrop-filter: blur(4px);
      }

      body.sidebar-open .sidebar-backdrop {
        opacity: 1;
        pointer-events: auto;
      }

      .workly-sidebar,
      .sidebar {
        position: fixed;
        top: 12px;
        left: 12px;
        bottom: 12px;
        z-index: 40;
        width: min(86vw, 320px);
        height: auto;
        display: grid;
        transform: translateX(calc(-100% - 24px));
        transition: transform 220ms cubic-bezier(.2,.8,.2,1);
        border-radius: 28px;
      }

      body.sidebar-open .workly-sidebar,
      body.sidebar-open .sidebar {
        transform: translateX(0);
      }

      .workly-collapse {
        display: grid;
      }

      .bottom-nav {
        display: none;
      }

      .main-wrap {
        padding-bottom: calc(20px + var(--safe-bottom));
      }
    }

  </style>
</head>
<body data-page="home">
  <div class="app-shell">
    <aside class="sidebar workly-sidebar" aria-label="Sidebar navigation">
      <div class="workly-top">
        <div class="sidebar-brand workly-brand">
          <div class="logo">A</div>
          <div>
            <div class="app-name">AyAstra</div>
            <div class="workly-caption">QuantaCore</div>
          </div>
        </div>
        <button class="workly-collapse" type="button" title="Close sidebar" aria-label="Close sidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 6l6 6-6 6"/></svg>
        </button>
      </div>

      <div class="workly-search" role="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="sidebarSearch" placeholder="Search..." />
        <span>⌘</span>
      </div>

      <nav class="nav-list workly-nav" id="sidebarNav"></nav>

      <div class="workly-other">
        <div class="recent-title">Other</div>
        <button type="button" class="workly-other-item">Documentation</button>
        <button type="button" class="workly-other-item">Inbox</button>
        <button type="button" class="workly-other-item">Support</button>
      </div>

      <div class="workly-spacer"></div>

      <div class="boost-card">
        <div class="boost-title">Boost with AI</div>
        <div class="boost-text">Source-backed replies, study help, and planning tools in one focused interface.</div>
        <button type="button" class="boost-button">Open QuantaCore</button>
      </div>

      <div class="user-card">
        <div class="user-avatar-small">AD</div>
        <div class="user-copy">
          <div>Ayanda D.</div>
          <span>Software Engineering</span>
        </div>
        <button type="button" class="user-menu" aria-label="User menu">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m6 9 6 6 6-6"/></svg>
        </button>
      </div>
    </aside>

    <div class="sidebar-backdrop" id="sidebarBackdrop" aria-hidden="true"></div>

    <main class="main-wrap">
      <header class="topbar">
        <button class="icon-btn sidebar-open-button" id="sidebarOpenButton" type="button" aria-label="Open sidebar" title="Open sidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></svg>
        </button>
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
          <div class="home-content">
            <div class="quanta-orb" aria-hidden="true">
              <div class="orb-wave"></div>
              <div class="orb-wave"></div>
              <div class="orb-wave"></div>
              <div class="quanta-core">
                <div class="orb-face" aria-hidden="true">
                  <span class="orb-eye orb-eye-left"></span>
                  <span class="orb-eye orb-eye-right"></span>
                  <span class="orb-smile"></span>
                  <span class="orb-blush orb-blush-left"></span>
                  <span class="orb-blush orb-blush-right"></span>
                </div>
                <div class="orb-particles" aria-hidden="true">
                  <span></span><span></span><span></span><span></span><span></span><span></span>
                </div>
              </div>
            </div>
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

              <div class="assistant-shortcuts" aria-label="AyAstra quick actions">
                <button class="shortcut-card" type="button" data-prompt="hello">
                  <span class="shortcut-icon">${icons.chats}</span>
                  <span>Chat with AyAstra</span>
                </button>
                <button class="shortcut-card" type="button" data-prompt="I want to talk to AyAstra by voice. Show me what voice features are available.">
                  <span class="shortcut-icon">${icons.mic}</span>
                  <span>Talk with AyAstra</span>
                </button>
              </div>

              <div class="topic-strip" aria-label="Topics">
                <button type="button" data-prompt="/news ai">AI</button>
                <button type="button" data-prompt="/tutor Python classes">Learn</button>
                <button type="button" data-prompt="Explain this coding concept step by step">Code</button>
                <button type="button" data-prompt="Help me plan my day">Life</button>
              </div>

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
      mic: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3Z"/><path d="M19 11a7 7 0 0 1-14 0"/><path d="M12 18v3"/><path d="M8 21h8"/></svg>',
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
    const sidebarOpenButton = document.getElementById('sidebarOpenButton');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');
    const sidebarCloseButton = document.querySelector('.workly-collapse');

    function openSidebar() {
      document.body.classList.add('sidebar-open');
      sidebarOpenButton?.setAttribute('aria-expanded', 'true');
    }

    function closeSidebar() {
      document.body.classList.remove('sidebar-open');
      sidebarOpenButton?.setAttribute('aria-expanded', 'false');
    }

    sidebarOpenButton?.addEventListener('click', openSidebar);
    sidebarBackdrop?.addEventListener('click', closeSidebar);
    sidebarCloseButton?.addEventListener('click', closeSidebar);

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeSidebar();
    });

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
        button.addEventListener('click', () => {
          setPage(button.dataset.nav);
          closeSidebar();
        });
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
        button.addEventListener('click', () => {
          setPage(button.dataset.pageTarget);
          closeSidebar();
        });
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

    let orbTimer = null;

    function setOrbMode(mode, duration = 0) {
      document.body.classList.remove('ai-thinking', 'ai-speaking');

      if (orbTimer) {
        clearTimeout(orbTimer);
        orbTimer = null;
      }

      if (mode === 'thinking') {
        document.body.classList.add('ai-thinking');
      }

      if (mode === 'speaking') {
        document.body.classList.add('ai-speaking');
      }

      if (duration > 0) {
        orbTimer = setTimeout(() => setOrbMode('idle'), duration);
      }
    }

    function speakingDurationFor(text) {
      return Math.min(7200, Math.max(1600, String(text || '').length * 24));
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
      setOrbMode('thinking');

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
        setOrbMode('speaking', speakingDurationFor(data.response));
      } catch (error) {
        removeTyping(typingId);
        state.messages.push({
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `AyAstra: Interface error: ${error.message}`,
          timestamp: timeNow()
        });
        renderPages();
        setOrbMode('speaking', 2400);
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
