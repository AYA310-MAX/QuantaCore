"""Local dashboard UI for AyAstra / QuantaCore.

This dashboard is the visual command-center version of AyAstra.
It runs locally at http://127.0.0.1:8765.

Design direction:
- cosmic purple/green/gold palette
- glassmorphism and geometric depth
- animated Siri/JARVIS-inspired QuantaCore orb
- local-only APIs for tasks, reminders, learning, news, research, and chat
"""

from __future__ import annotations

import json
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from ay_astra.assistant import handle_message
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

    def do_GET(self) -> None:  # noqa: N802
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/":
            self._send_html(DASHBOARD_HTML)
            return

        if path == "/api/state":
            self._send_json(build_dashboard_state())
            return

        if path == "/api/news":
            topic = urllib.parse.parse_qs(parsed_url.query).get("topic", ["technology"])[0]
            self._send_json({"text": get_news_brief(topic)})
            return

        if path == "/api/research":
            topic = urllib.parse.parse_qs(parsed_url.query).get("topic", [""])[0]
            self._send_json({"text": get_research_brief(topic)})
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        payload = self._read_json_body()

        if path == "/api/chat":
            message = str(payload.get("message", "")).strip()
            if not message:
                self._send_json(
                    {
                        "response": "AyAstra: Say something first, genius. I cannot process atmospheric silence.",
                        "state": build_dashboard_state(),
                    }
                )
                return

            response = handle_message(message)
            if response == "__EXIT__":
                response = "AyAstra: Dashboard mode stays online. Press Ctrl+C in the dashboard terminal to stop the server."

            self._send_json({"response": response, "state": build_dashboard_state()})
            return

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
        return

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0") or 0)
        if content_length <= 0:
            return {}

        try:
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
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
    tasks = load_json(TASKS_PATH, [])
    reminders = load_json(REMINDERS_PATH, [])
    learning_log = load_json(LEARNING_LOG_PATH, [])

    pending_tasks = [task for task in tasks if not task.get("done")]
    pending_reminders = [reminder for reminder in reminders if not reminder.get("delivered")]
    total_reviews = sum(int(entry.get("times_reviewed", 0) or 0) for entry in learning_log)

    return {
        "stats": {
            "tasks_total": len(tasks),
            "tasks_pending": len(pending_tasks),
            "reminders_total": len(reminders),
            "reminders_pending": len(pending_reminders),
            "learning_topics": len(learning_log),
            "learning_reviews": total_reviews,
        },
        "tasks": tasks,
        "reminders": reminders,
        "learning_log": learning_log,
    }


def run_dashboard(host: str = HOST, port: int = PORT, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    url = f"http://{host}:{port}"

    print("AyAstra Dashboard online — QuantaCore geometric interface active.")
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


DASHBOARD_HTML = r'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AyAstra // QuantaCore Geometric Interface</title>
  <style>
    :root {
      --void: #03040b;
      --obsidian: #080a13;
      --purple-950: #16001f;
      --purple-900: #1f0035;
      --purple-700: #390040;
      --violet: #5a0060;
      --neon: #ec5cff;
      --amethyst: #a855f7;
      --cyan: #67e8f9;
      --mint: #569578;
      --emerald: #275d46;
      --green-black: #101c13;
      --gold: #c7940e;
      --peach: #ed9e6f;
      --rose: #b66570;
      --text: #fff5ff;
      --muted: #bca8ce;
      --glass: rgba(20, 13, 36, 0.56);
      --glass-2: rgba(58, 24, 83, 0.34);
      --line: rgba(255, 255, 255, 0.17);
      --line-hot: rgba(236, 92, 255, 0.42);
      --depth-shadow: 0 28px 80px rgba(0, 0, 0, 0.38), 0 0 42px rgba(168, 85, 247, 0.15);
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      min-height: 100vh;
      overflow-x: hidden;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 15% 15%, rgba(90, 0, 96, 0.55), transparent 28%),
        radial-gradient(circle at 80% 10%, rgba(103, 232, 249, 0.16), transparent 24%),
        radial-gradient(circle at 75% 82%, rgba(199, 148, 14, 0.13), transparent 32%),
        radial-gradient(circle at 22% 88%, rgba(39, 93, 70, 0.25), transparent 32%),
        linear-gradient(135deg, #03040b 0%, #12051f 45%, #06110e 100%);
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: 0.17;
      background-image:
        linear-gradient(rgba(255,255,255,0.13) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.13) 1px, transparent 1px),
        linear-gradient(60deg, rgba(236,92,255,0.09) 1px, transparent 1px),
        linear-gradient(120deg, rgba(103,232,249,0.06) 1px, transparent 1px);
      background-size: 68px 68px, 68px 68px, 128px 128px, 128px 128px;
      mask-image: linear-gradient(to bottom, black 0%, transparent 92%);
    }

    body::after {
      content: "";
      position: fixed;
      inset: -20%;
      pointer-events: none;
      background: conic-gradient(from 0deg at 50% 50%, transparent, rgba(236,92,255,0.16), transparent, rgba(103,232,249,0.11), transparent, rgba(199,148,14,0.11), transparent);
      filter: blur(60px);
      animation: cosmicSpin 34s linear infinite;
    }

    @keyframes cosmicSpin { to { transform: rotate(360deg); } }

    .starfield {
      position: fixed;
      inset: 0;
      pointer-events: none;
      opacity: .32;
      background-image:
        radial-gradient(circle, rgba(255,255,255,.86) 0 1px, transparent 1.4px),
        radial-gradient(circle, rgba(236,92,255,.7) 0 1px, transparent 1.5px),
        radial-gradient(circle, rgba(103,232,249,.65) 0 1px, transparent 1.6px);
      background-size: 180px 180px, 260px 260px, 340px 340px;
      background-position: 20px 30px, 80px 140px, 210px 50px;
      animation: driftStars 42s linear infinite;
    }

    @keyframes driftStars { to { transform: translate3d(-70px, 40px, 0); } }

    .shell {
      position: relative;
      z-index: 2;
      width: min(1500px, calc(100% - 30px));
      margin: auto;
      padding: 22px 0 44px;
      perspective: 1400px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      margin-bottom: 18px;
      transform-style: preserve-3d;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .sigil {
      width: 48px;
      height: 48px;
      border-radius: 18px;
      position: relative;
      background: radial-gradient(circle at 35% 25%, #fff, var(--cyan) 8%, var(--neon) 28%, var(--violet) 55%, var(--void) 78%);
      box-shadow: 0 0 30px rgba(236,92,255,.55), inset 0 0 18px rgba(255,255,255,.22);
      transform: rotate(45deg);
    }

    .sigil::before, .sigil::after {
      content: "";
      position: absolute;
      inset: 8px;
      border: 1px solid rgba(255,255,255,.45);
      clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%);
    }

    .sigil::after { inset: 15px; opacity: .65; }

    .brand strong {
      display: block;
      letter-spacing: .18em;
      text-transform: uppercase;
      font-size: .86rem;
    }

    .brand span {
      color: var(--muted);
      font-size: .82rem;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 11px 14px;
      border: 1px solid rgba(255,255,255,.17);
      border-radius: 999px;
      background: rgba(255,255,255,.065);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.11), 0 0 22px rgba(103,232,249,.08);
      color: #f6eaff;
      backdrop-filter: blur(18px);
    }

    .holo-stage {
      display: grid;
      grid-template-columns: minmax(0, 1.22fr) minmax(360px, .78fr);
      gap: 18px;
      margin-bottom: 18px;
      transform-style: preserve-3d;
    }

    .glass {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      background:
        linear-gradient(135deg, rgba(255,255,255,.08), rgba(255,255,255,.018) 42%, rgba(255,255,255,.05)),
        linear-gradient(145deg, var(--glass), rgba(8, 10, 20, .58));
      box-shadow: var(--depth-shadow), inset 0 1px 0 rgba(255,255,255,.12);
      backdrop-filter: blur(24px);
      border-radius: 34px;
      transform-style: preserve-3d;
    }

    .glass::before {
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      background:
        linear-gradient(90deg, transparent, rgba(255,255,255,.09), transparent),
        repeating-linear-gradient(0deg, rgba(255,255,255,.035) 0 1px, transparent 1px 10px);
      opacity: .5;
      mix-blend-mode: screen;
    }

    .glass::after {
      content: "";
      position: absolute;
      inset: 14px;
      pointer-events: none;
      border: 1px solid rgba(255,255,255,.07);
      border-radius: 26px;
      clip-path: polygon(0 0, 35% 0, 35% 1px, 100% 1px, 100% 100%, 65% 100%, 65% calc(100% - 1px), 0 calc(100% - 1px));
    }

    .hero-copy {
      min-height: 500px;
      padding: clamp(28px, 4vw, 54px);
      transform: rotateX(1deg) rotateY(-1.2deg);
    }

    .hero-copy .geo-label {
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 22px;
      color: var(--cyan);
      letter-spacing: .22em;
      text-transform: uppercase;
      font-size: .72rem;
    }

    .geo-label::before {
      content: "";
      width: 36px;
      height: 1px;
      background: linear-gradient(90deg, var(--cyan), transparent);
    }

    h1 {
      margin: 0 0 20px;
      max-width: 850px;
      font-size: clamp(3.1rem, 8vw, 8.4rem);
      line-height: .78;
      letter-spacing: -.085em;
      text-transform: uppercase;
    }

    .grad {
      background: linear-gradient(90deg, #fff, var(--neon), var(--amethyst), var(--cyan));
      background-size: 220% 100%;
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      animation: gradientFlow 6s ease-in-out infinite alternate;
    }

    @keyframes gradientFlow { to { background-position: 100% 0; } }

    .lead {
      position: relative;
      z-index: 1;
      max-width: 780px;
      color: #dccce9;
      line-height: 1.75;
      font-size: 1.03rem;
    }

    .hero-actions {
      position: relative;
      z-index: 1;
      display: flex;
      flex-wrap: wrap;
      gap: 11px;
      margin-top: 26px;
    }

    button, input, textarea { font: inherit; }

    button {
      cursor: pointer;
      border: 0;
      border-radius: 17px;
      padding: 12px 15px;
      color: #14051d;
      font-weight: 900;
      background: linear-gradient(90deg, var(--neon), var(--amethyst), var(--cyan));
      box-shadow: 0 0 24px rgba(168,85,247,.23), inset 0 1px 0 rgba(255,255,255,.36);
      transition: transform .18s ease, filter .18s ease, box-shadow .18s ease;
    }

    button:hover {
      transform: translateY(-2px);
      filter: brightness(1.09);
      box-shadow: 0 0 34px rgba(236,92,255,.34);
    }

    button.secondary {
      color: var(--text);
      border: 1px solid rgba(255,255,255,.16);
      background: rgba(255,255,255,.07);
    }

    button.gold { background: linear-gradient(90deg, var(--gold), var(--peach)); color: #1a0d06; }

    .geo-object {
      position: absolute;
      pointer-events: none;
      opacity: .72;
      filter: drop-shadow(0 0 22px rgba(236,92,255,.2));
    }

    .geo-object.one {
      right: 7%;
      top: 9%;
      width: 190px;
      height: 190px;
      border: 1px solid rgba(236,92,255,.25);
      clip-path: polygon(50% 0, 100% 22%, 84% 100%, 16% 100%, 0 22%);
      animation: floatGeo 7s ease-in-out infinite;
    }

    .geo-object.two {
      right: 19%;
      bottom: 8%;
      width: 120px;
      height: 120px;
      border: 1px solid rgba(103,232,249,.22);
      transform: rotate(45deg);
      animation: floatGeo 9s ease-in-out infinite reverse;
    }

    @keyframes floatGeo { 50% { transform: translateY(-18px) rotate(9deg); } }

    .core-panel {
      min-height: 500px;
      display: grid;
      place-items: center;
      padding: 24px;
      transform: rotateX(1deg) rotateY(1.8deg) translateZ(14px);
    }

    .core-title, .core-status {
      position: absolute;
      z-index: 2;
      top: 26px;
      letter-spacing: .18em;
      text-transform: uppercase;
      font-size: .76rem;
    }

    .core-title { left: 28px; color: #ffeaff; font-weight: 900; }
    .core-status { right: 28px; color: var(--cyan); }

    .orb-wrap {
      position: relative;
      width: min(390px, 82vw);
      aspect-ratio: 1;
      display: grid;
      place-items: center;
      transform-style: preserve-3d;
    }

    .orb-wrap::before, .orb-wrap::after {
      content: "";
      position: absolute;
      border-radius: 50%;
      border: 1px solid rgba(255,255,255,.16);
      transform-style: preserve-3d;
    }

    .orb-wrap::before {
      inset: 2%;
      transform: rotateX(68deg) rotateZ(12deg);
      box-shadow: 0 0 70px rgba(103,232,249,.12) inset;
      animation: orbitTilt 9s linear infinite;
    }

    .orb-wrap::after {
      inset: 15%;
      transform: rotateX(72deg) rotateZ(-25deg);
      border-color: rgba(236,92,255,.27);
      animation: orbitTilt 6s linear infinite reverse;
    }

    @keyframes orbitTilt { to { rotate: 360deg; } }

    .core-sphere {
      position: relative;
      width: 58%;
      aspect-ratio: 1;
      border-radius: 50%;
      background:
        radial-gradient(circle at 38% 30%, #ffffff 0 2%, #bffcff 4% 8%, #ec5cff 17%, rgba(90,0,96,.86) 42%, rgba(3,4,11,.94) 72%),
        conic-gradient(from 80deg, var(--cyan), var(--neon), var(--gold), var(--mint), var(--cyan));
      box-shadow:
        0 0 22px rgba(255,255,255,.25) inset,
        0 0 55px rgba(236,92,255,.72),
        0 0 110px rgba(103,232,249,.2);
      transform-style: preserve-3d;
      animation: sphereFloat 5.4s ease-in-out infinite;
    }

    .core-sphere::before {
      content: "";
      position: absolute;
      inset: -10%;
      border-radius: inherit;
      background:
        conic-gradient(from 0deg, transparent 0 8%, rgba(103,232,249,.95) 10%, transparent 13% 24%, rgba(236,92,255,.9) 28%, transparent 32% 48%, rgba(199,148,14,.8) 52%, transparent 56% 74%, rgba(86,149,120,.85) 78%, transparent 82% 100%);
      filter: blur(7px);
      opacity: .82;
      mix-blend-mode: screen;
      animation: spin 3.8s linear infinite;
    }

    .core-sphere::after {
      content: "";
      position: absolute;
      inset: 9%;
      border-radius: inherit;
      border: 1px solid rgba(255,255,255,.24);
      background:
        linear-gradient(35deg, transparent 44%, rgba(255,255,255,.32) 45%, transparent 47%),
        linear-gradient(125deg, transparent 42%, rgba(103,232,249,.22) 43%, transparent 46%);
      opacity: .72;
      animation: facetShift 5s ease-in-out infinite alternate;
    }

    .orb-wrap.speaking .core-sphere {
      animation: sphereTalk .95s ease-in-out infinite;
    }

    .orb-wrap.speaking .core-sphere::before { animation-duration: 1.25s; opacity: 1; }

    .wave {
      position: absolute;
      inset: 26%;
      border-radius: 50%;
      border: 1px solid rgba(236,92,255,.38);
      opacity: 0;
    }

    .orb-wrap.speaking .wave { animation: waveOut 1.25s ease-out infinite; }
    .orb-wrap.speaking .wave:nth-child(2) { animation-delay: .22s; border-color: rgba(103,232,249,.35); }
    .orb-wrap.speaking .wave:nth-child(3) { animation-delay: .44s; border-color: rgba(199,148,14,.32); }

    .node {
      position: absolute;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--cyan);
      box-shadow: 0 0 18px var(--cyan);
    }

    .node.n1 { top: 14%; left: 48%; }
    .node.n2 { right: 17%; top: 50%; background: var(--neon); box-shadow: 0 0 18px var(--neon); }
    .node.n3 { bottom: 18%; left: 28%; background: var(--gold); box-shadow: 0 0 18px var(--gold); }

    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes sphereFloat { 50% { transform: translateY(-15px) rotateX(8deg) rotateY(-10deg) scale(1.03); } }
    @keyframes sphereTalk { 0%,100% { transform: scale(1) rotateX(0) rotateY(0); } 35% { transform: scale(1.12,.94) rotateX(7deg); } 70% { transform: scale(.96,1.1) rotateY(-9deg); } }
    @keyframes facetShift { to { transform: rotate(18deg) scale(1.03); } }
    @keyframes waveOut { 0% { opacity: .85; transform: scale(.74); } 100% { opacity: 0; transform: scale(1.85); } }

    .telemetry {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }

    .stat {
      min-height: 125px;
      padding: 18px;
      border-radius: 26px;
      transform: translateZ(0);
    }

    .label {
      color: var(--muted);
      font-size: .72rem;
      letter-spacing: .17em;
      text-transform: uppercase;
    }

    .value {
      font-size: 2.65rem;
      font-weight: 950;
      margin-top: 8px;
      text-shadow: 0 0 20px rgba(236,92,255,.3);
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 16px;
      align-items: start;
    }

    .panel {
      grid-column: span 4;
      padding: 18px;
      min-height: 294px;
      border-radius: 28px;
      transform: translateZ(0);
    }

    .panel:hover { transform: translateY(-2px) rotateX(.8deg); }
    .wide { grid-column: span 8; }
    .chat { grid-column: span 5; }
    .research { grid-column: span 7; }

    .panel h2 {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin: 0 0 14px;
      font-size: .96rem;
      letter-spacing: .12em;
      text-transform: uppercase;
    }

    .tag { color: var(--gold); font-size: .76rem; }

    form, .control {
      display: grid;
      gap: 9px;
      margin-bottom: 14px;
    }

    .two { grid-template-columns: 1fr 1fr; }

    input, textarea {
      width: 100%;
      border: 1px solid rgba(255,255,255,.14);
      border-radius: 16px;
      background: rgba(4, 5, 16, .62);
      color: var(--text);
      padding: 12px 13px;
      outline: none;
    }

    input:focus, textarea:focus {
      border-color: var(--neon);
      box-shadow: 0 0 0 3px rgba(236,92,255,.12), 0 0 18px rgba(236,92,255,.16);
    }

    .list {
      display: grid;
      gap: 10px;
      max-height: 365px;
      overflow: auto;
      padding-right: 3px;
    }

    .item {
      position: relative;
      border: 1px solid rgba(255,255,255,.12);
      background: rgba(255,255,255,.055);
      border-radius: 18px;
      padding: 12px;
      overflow: hidden;
    }

    .item::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 3px;
      background: linear-gradient(var(--neon), var(--cyan));
      opacity: .9;
    }

    .item.done { opacity: .58; }

    .item-title {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
    }

    .meta {
      color: var(--muted);
      font-size: .86rem;
      line-height: 1.45;
      margin-top: 5px;
    }

    pre {
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      color: #f9efff;
      line-height: 1.52;
      max-height: 430px;
      overflow: auto;
      padding: 15px;
      border-radius: 19px;
      border: 1px solid rgba(255,255,255,.12);
      background:
        linear-gradient(135deg, rgba(236,92,255,.07), rgba(103,232,249,.035)),
        rgba(4,5,16,.64);
    }

    .chat-log {
      height: 420px;
      overflow: auto;
      display: grid;
      align-content: start;
      gap: 10px;
      margin-bottom: 14px;
      padding-right: 3px;
    }

    .bubble {
      max-width: 92%;
      padding: 12px 14px;
      border-radius: 18px;
      line-height: 1.52;
    }

    .bubble.user {
      justify-self: end;
      border: 1px solid rgba(103,232,249,.24);
      background: rgba(103,232,249,.12);
    }

    .bubble.astra {
      justify-self: start;
      border: 1px solid rgba(236,92,255,.25);
      background: rgba(236,92,255,.12);
    }

    .toast {
      position: fixed;
      left: 50%;
      bottom: 22px;
      z-index: 30;
      transform: translateX(-50%);
      width: min(760px, calc(100% - 28px));
      padding: 14px 16px;
      border-radius: 18px;
      border: 1px solid rgba(236,92,255,.35);
      background: rgba(15, 10, 28, .92);
      box-shadow: var(--depth-shadow);
      color: var(--text);
      opacity: 0;
      pointer-events: none;
      transition: opacity .2s ease;
      backdrop-filter: blur(18px);
    }

    .toast.show { opacity: 1; }

    @media (max-width: 1100px) {
      .holo-stage { grid-template-columns: 1fr; }
      .hero-copy, .core-panel { transform: none; }
      .telemetry { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .grid { grid-template-columns: 1fr; }
      .panel, .wide, .chat, .research { grid-column: auto; }
      .two { grid-template-columns: 1fr; }
    }

    @media (max-width: 620px) {
      .topbar { align-items: flex-start; flex-direction: column; }
      .hero-copy { min-height: auto; }
      .telemetry { grid-template-columns: 1fr; }
      h1 { font-size: clamp(2.6rem, 18vw, 4.3rem); }
      .orb-wrap { width: min(330px, 88vw); }
    }
  </style>
</head>
<body>
  <div class="starfield"></div>
  <main class="shell">
    <nav class="topbar">
      <div class="brand">
        <div class="sigil" aria-hidden="true"></div>
        <div>
          <strong>AyAstra</strong>
          <span>QuantaCore // geometric lab interface</span>
        </div>
      </div>
      <div class="pill" id="connectionPill">Local lab online</div>
    </nav>

    <section class="holo-stage">
      <article class="glass hero-copy">
        <div class="geo-label">Astra Protocol // Student Command Layer</div>
        <h1>Not a dashboard. <span class="grad">A command dimension.</span></h1>
        <p class="lead">
          AyAstra is your Shuri-inspired personal AI lab: source-backed news, research, planning,
          learning logs, quizzes, and a living QuantaCore sphere that reacts while she thinks and speaks.
          Less spreadsheet. More orbital intelligence.
        </p>
        <div class="hero-actions">
          <button onclick="focusChat()">Open Chat Channel</button>
          <button class="secondary" onclick="quickChat('/news ai')">AI Intel Feed</button>
          <button class="gold" onclick="quickChat('/learn review')">Review Queue</button>
        </div>
        <div class="geo-object one"></div>
        <div class="geo-object two"></div>
      </article>

      <aside class="glass core-panel">
        <div class="core-title">QUANTACORE</div>
        <div class="core-status" id="coreStatus">idle</div>
        <div class="orb-wrap" id="orbWrap" aria-label="Animated QuantaCore visual sphere">
          <div class="wave"></div>
          <div class="wave"></div>
          <div class="wave"></div>
          <div class="node n1"></div>
          <div class="node n2"></div>
          <div class="node n3"></div>
          <div class="core-sphere"></div>
        </div>
        <label class="pill">
          <input type="checkbox" id="voiceToggle" /> browser voice + reactive core
        </label>
      </aside>
    </section>

    <section class="telemetry">
      <div class="glass stat"><div class="label">Pending tasks</div><div class="value" id="tasksPending">0</div></div>
      <div class="glass stat"><div class="label">Reminders</div><div class="value" id="remindersPending">0</div></div>
      <div class="glass stat"><div class="label">Learning topics</div><div class="value" id="learningTopics">0</div></div>
      <div class="glass stat"><div class="label">Reviews</div><div class="value" id="learningReviews">0</div></div>
    </section>

    <section class="grid">
      <section class="glass panel chat">
        <h2>Conversation Core <span class="tag">Live</span></h2>
        <div class="chat-log" id="chatLog">
          <div class="bubble astra">AyAstra online. QuantaCore is stable. Ask me something, or pretend you were not procrastinating. I have sensors.</div>
        </div>
        <form id="chatForm" class="control two">
          <input id="chatInput" placeholder="Try: /news ai, /research CRISPR, explain APIs" />
          <button>Transmit</button>
        </form>
        <div class="control two">
          <button class="secondary" onclick="quickChat('/task list')">Task Scan</button>
          <button class="secondary" onclick="quickChat('/quiz feedback')">Feedback Scan</button>
        </div>
      </section>

      <section class="glass panel">
        <h2>Task Matrix <span class="tag">Planner</span></h2>
        <form id="taskForm">
          <input id="taskInput" placeholder="e.g. Finish AI assignment" />
          <button>Add Task</button>
        </form>
        <div class="list" id="tasksList"></div>
      </section>

      <section class="glass panel">
        <h2>Timeline Nodes <span class="tag">Reminders</span></h2>
        <form id="reminderForm">
          <input id="reminderDate" type="datetime-local" />
          <input id="reminderMessage" placeholder="Reminder message" />
          <button>Add Reminder</button>
        </form>
        <div class="list" id="remindersList"></div>
      </section>

      <section class="glass panel">
        <h2>Knowledge Vault <span class="tag">Learning</span></h2>
        <form id="learnForm">
          <input id="learnTopic" placeholder="Topic, e.g. APIs" />
          <textarea id="learnNote" rows="3" placeholder="Note, e.g. APIs let apps talk"></textarea>
          <button>Add Topic</button>
        </form>
        <div class="list" id="learningList"></div>
      </section>

      <section class="glass panel wide">
        <h2>Verified Signal Feed <span class="tag">News</span></h2>
        <div class="control two">
          <input id="newsTopic" value="ai" placeholder="Topic, e.g. ai, tech, south africa" />
          <button id="newsButton">Fetch Source Feed</button>
        </div>
        <pre id="newsOutput">Click “Fetch Source Feed” to load source-backed headlines.</pre>
      </section>

      <section class="glass panel research">
        <h2>Research Telescope <span class="tag">Academic</span></h2>
        <div class="control two">
          <input id="researchTopic" value="AI agents in education" placeholder="Research topic" />
          <button id="researchButton">Search Papers</button>
        </div>
        <pre id="researchOutput">Search a research topic to load paper metadata and links.</pre>
      </section>
    </section>
  </main>

  <div class="toast" id="toast"></div>

  <script>
    const $ = (id) => document.getElementById(id);
    const orb = $('orbWrap');
    const status = $('coreStatus');

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

    function setCoreMode(mode = 'idle') {
      status.textContent = mode;
      orb.classList.toggle('speaking', mode === 'speaking' || mode === 'thinking');
    }

    function pulseCore(text = '') {
      setCoreMode('speaking');
      const ms = Math.min(6200, Math.max(1300, String(text).length * 22));
      setTimeout(() => setCoreMode('idle'), ms);
    }

    function speak(text) {
      const clean = String(text)
        .replace(/^AyAstra:\s*/i, '')
        .replace(/https?:\/\/\S+/g, 'link available in the dashboard')
        .slice(0, 950);

      if (!$('voiceToggle').checked || !('speechSynthesis' in window)) {
        pulseCore(clean);
        return;
      }

      speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(clean);
      utterance.rate = 0.98;
      utterance.pitch = 1.05;
      utterance.onstart = () => setCoreMode('speaking');
      utterance.onend = () => setCoreMode('idle');
      utterance.onerror = () => setCoreMode('idle');
      speechSynthesis.speak(utterance);
    }

    async function apiGet(url) {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      return response.json();
    }

    async function apiPost(url, data) {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      return response.json();
    }

    function renderState(state) {
      $('connectionPill').textContent = 'Local lab online // private interface';
      $('tasksPending').textContent = state.stats.tasks_pending;
      $('remindersPending').textContent = state.stats.reminders_pending;
      $('learningTopics').textContent = state.stats.learning_topics;
      $('learningReviews').textContent = state.stats.learning_reviews;
      renderTasks(state.tasks || []);
      renderReminders(state.reminders || []);
      renderLearning(state.learning_log || []);
    }

    function renderTasks(tasks) {
      $('tasksList').innerHTML = tasks.length
        ? tasks.map(task => `
          <div class="item ${task.done ? 'done' : ''}">
            <div class="item-title">
              <b>${task.done ? '✅' : '⬜'} #${task.id}: ${escapeHtml(task.description)}</b>
              ${task.done ? '' : `<button class="secondary" onclick="completeTask(${task.id})">Done</button>`}
            </div>
            <div class="meta">Created: ${escapeHtml(task.created_at || 'unknown')}</div>
          </div>`).join('')
        : '<div class="item"><div class="meta">No tasks yet. Suspiciously peaceful.</div></div>';
    }

    function renderReminders(reminders) {
      $('remindersList').innerHTML = reminders.length
        ? reminders.map(reminder => `
          <div class="item ${reminder.delivered ? 'done' : ''}">
            <b>${reminder.delivered ? '✅' : '⏰'} #${reminder.id}: ${escapeHtml(reminder.message)}</b>
            <div class="meta">When: ${escapeHtml(reminder.remind_at || 'unknown')}</div>
          </div>`).join('')
        : '<div class="item"><div class="meta">No reminders yet. Timeline clean.</div></div>';
    }

    function renderLearning(entries) {
      $('learningList').innerHTML = entries.length
        ? entries.map(entry => `
          <div class="item">
            <b>#${entry.id}: ${escapeHtml(entry.topic)}</b>
            <div class="meta">${escapeHtml(entry.note || 'No note saved')}</div>
            <div class="meta">Reviews: ${entry.times_reviewed || 0} • Last reviewed: ${escapeHtml(entry.last_reviewed_at || 'never')}</div>
          </div>`).join('')
        : '<div class="item"><div class="meta">Learning archive empty. Feed the vault.</div></div>';
    }

    async function loadState() {
      try {
        renderState(await apiGet('/api/state'));
      } catch (error) {
        showToast(`Dashboard load failed: ${error.message}`);
      }
    }

    async function completeTask(id) {
      setCoreMode('thinking');
      const data = await apiPost('/api/task/done', { id });
      showToast(data.message);
      renderState(data.state);
      speak(data.message);
    }

    function appendChat(role, text) {
      const bubble = document.createElement('div');
      bubble.className = `bubble ${role}`;
      bubble.textContent = text;
      $('chatLog').appendChild(bubble);
      $('chatLog').scrollTop = $('chatLog').scrollHeight;
    }

    async function sendChat(message) {
      const text = String(message || '').trim();
      if (!text) return;
      appendChat('user', text);
      setCoreMode('thinking');
      try {
        const data = await apiPost('/api/chat', { message: text });
        appendChat('astra', data.response);
        renderState(data.state);
        speak(data.response);
      } catch (error) {
        appendChat('astra', `AyAstra: Chat channel failed: ${error.message}`);
        setCoreMode('idle');
      }
    }

    function focusChat() { $('chatInput').focus(); }
    function quickChat(message) { sendChat(message); }

    $('chatForm').addEventListener('submit', (event) => {
      event.preventDefault();
      const message = $('chatInput').value;
      $('chatInput').value = '';
      sendChat(message);
    });

    $('taskForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const description = $('taskInput').value.trim();
      if (!description) return showToast('Task description missing. Even futuristic interfaces need details.');
      setCoreMode('thinking');
      const data = await apiPost('/api/task/add', { description });
      $('taskInput').value = '';
      showToast(data.message);
      renderState(data.state);
      speak(data.message);
    });

    $('learnForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const topic = $('learnTopic').value.trim();
      const note = $('learnNote').value.trim();
      if (!topic) return showToast('Topic missing. The vault cannot store vibes only.');
      setCoreMode('thinking');
      const data = await apiPost('/api/learn/add', { topic, note });
      $('learnTopic').value = '';
      $('learnNote').value = '';
      showToast(data.message);
      renderState(data.state);
      speak(data.message);
    });

    $('reminderForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const datetime = $('reminderDate').value;
      const message = $('reminderMessage').value.trim();
      if (!datetime || !message) return showToast('Reminder details missing. Time travel still requires timestamps.');
      setCoreMode('thinking');
      const data = await apiPost('/api/reminder/add', { datetime, message });
      $('reminderMessage').value = '';
      showToast(data.message);
      renderState(data.state);
      speak(data.message);
    });

    $('newsButton').addEventListener('click', async () => {
      const topic = $('newsTopic').value.trim() || 'technology';
      $('newsOutput').textContent = 'Fetching source-backed signal feed...';
      setCoreMode('thinking');
      try {
        const data = await apiGet(`/api/news?topic=${encodeURIComponent(topic)}`);
        $('newsOutput').textContent = data.text;
        speak(data.text);
      } catch (error) {
        $('newsOutput').textContent = `News fetch failed: ${error.message}`;
        setCoreMode('idle');
      }
    });

    $('researchButton').addEventListener('click', async () => {
      const topic = $('researchTopic').value.trim();
      if (!topic) return showToast('Research topic missing. Even scholars need a target.');
      $('researchOutput').textContent = 'Searching academic metadata through the telescope...';
      setCoreMode('thinking');
      try {
        const data = await apiGet(`/api/research?topic=${encodeURIComponent(topic)}`);
        $('researchOutput').textContent = data.text;
        speak(data.text);
      } catch (error) {
        $('researchOutput').textContent = `Research search failed: ${error.message}`;
        setCoreMode('idle');
      }
    });

    loadState();
    setInterval(loadState, 15000);
  </script>
</body>
</html>
'''
