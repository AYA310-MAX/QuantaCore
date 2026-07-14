from flask import Flask, render_template, request, jsonify
from quantacore.assistant import Assistant

app = Flask(__name__)
assistant = Assistant()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "..."})

    reply = assistant.handle_message(message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=8765)