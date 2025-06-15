from flask import Flask, request, render_template
from openai_client import get_openrouter_client
import traceback

app = Flask(__name__)
client = get_openrouter_client()

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        try:
            user_input = request.form["message"]

            # Gọi API OpenRouter
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1024,
                temperature=0.7
            )

            # In kết quả ra Logs để kiểm tra
            print("📥 AI response:", response)

            # Trích xuất câu trả lời
            reply = response.choices[0].message.content

        except Exception as e:
            # In lỗi ra Logs và phản hồi lên giao diện
            print("❌ Lỗi khi gọi API:", traceback.format_exc())
            reply = f"<pre>Lỗi máy chủ nội bộ:\n{traceback.format_exc()}</pre>"

    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
