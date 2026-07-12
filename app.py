from flask import Flask, render_template, request, jsonify
from quantacore.assistant import Assistant

app = Flask(__name__)

# Create one assistant instance
assistant = Assistant()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"reply": "I didn't receive a message."})

    reply = assistant.handle_message(user_message)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=8765)