# backend/rag/search.py
#search.py …… RAGの司令塔であり、資料室に検索依頼して、vectorからもらった関連度の高い文章をまとめたテキストにして、app.pyにデータを返している。
from .embed import embed_text
from .vector_store import query_similar

def retrieve_answer(query: str):
    """
    ユーザー質問から、
    1) 埋め込みを作り
    2) 類似文書を検索し
    3) まとめた文章を返す（まだLLMには投げない）
    """
    # 1. 質問を埋め込みに
    q_emb = embed_text(query)

    # 2. ベクトルDBに検索依頼
    result = query_similar(q_emb, top_k=3)

    docs = result.get("documents", [[]])[0]  # [['doc1', 'doc2'...]] の形なので最初のリストだけ取る

    # 3. 上位文書をまとめる
    if not docs:
        return "関連する資料が見つかりませんでした。"

    summary = "【RAGから取得した関連資料】\n"
    for i, d in enumerate(docs):
        summary += f"\n--- 文書 {i+1} ---\n{d}\n"

    # → この summary を LLM に投げれば「資料を読んだ回答」ができる
    return summary