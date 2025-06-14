from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env (nếu có)
load_dotenv()

# Gán API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo Flask app
app = Flask(__name__)

# Trang chính: hiển thị giao diện + xử lý form hỏi/đáp
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Bạn có thể thay bằng model khác nếu muốn
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"❌ Lỗi khi gọi API: {str(e)}"
    return render_template("index.html", answer=answer)

# Chạy ứng dụng Flask trên host và port yêu cầu của Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
