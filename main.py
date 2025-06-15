from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Lấy API key và tên mô hình từ biến môi trường
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")

@app.route("/", methods=["GET"])
def index():
    return "✅ AI Agent đang hoạt động trên Render!"

@app.route("/hoi", methods=["POST"])
def hoi():
    try:
        user_input = request.json.get("prompt", "")
        if not user_input:
            return jsonify({"error": "Thiếu prompt"}), 400

        # Gọi API OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            }
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render tự cấp biến PORT
    app.run(host="0.0.0.0", port=port)
