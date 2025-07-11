from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}]
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Oops! Something went wrong.\nError: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
