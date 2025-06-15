import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 🔄 Tải biến môi trường từ file .env (nếu có)

def get_openrouter_client():
    return OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
