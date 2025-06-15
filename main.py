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
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",  # 🔁 Có thể thay bằng gemini hoặc mistral
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            reply = response.choices[0].message.content
        except Exception:
            reply = f"<pre>{traceback.format_exc()}</pre>"
    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
