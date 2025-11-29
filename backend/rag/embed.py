# backend/rag/embed.py
#embed.py …… 文章を機械が読める形に変換する人。ベクトルに変換する作業
from openai import OpenAI
import os

# 環境変数 OPENAI_API_KEY を使う想定
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text: str):
    """
    テキストを埋め込み（数値ベクトル）に変換して返す。
    """
    if not text.strip():
        return []

    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return res.data[0].embedding  # ベクトル（list[float]）