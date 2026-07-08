"""
app.py — Flask server for the Explainable Clinical NLP Chatbot.
"""
from dotenv import load_dotenv
import os

load_dotenv()
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from manager import process_message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical-chatbot-dev-key")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_text = data.get("message", "").strip()

    if not user_text:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        result = process_message(user_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "medical-chatbot"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)