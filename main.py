from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Lấy API key và tên model từ biến môi trường
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")

# Route hiển thị giao diện web
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Tìm trong thư mục /templates/

# Route xử lý câu hỏi từ người dùng
@app.route("/hoi", methods=["POST"])
def hoi():
    try:
        user_input = request.json.get("prompt", "")
        if not user_input:
            return jsonify({"error": "⚠️ Bạn chưa nhập nội dung."}), 400

        # Gửi yêu cầu tới OpenRouter
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
        return jsonify({"error": f"Lỗi hệ thống: {str(e)}"}), 500

# Khởi động ứng dụng trên Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render tự cấp PORT
    app.run(host="0.0.0.0", port=port)
