# backend/rag/vector_store.py
#vector_store.py …… 資料室そのもの（ChromaDB）、ベクトルを保存する。

import chromadb
from chromadb.utils import embedding_functions

# ChromaDBのクライアント
client = chromadb.Client()

# コレクション（データベース）作成
collection = client.get_or_create_collection(
    name="my_docs",
)

def add_document(doc_id: str, text: str, embedding: list):
    """
    新しい文書をベクトルDBに追加する
    """
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
    )

def query_similar(query_emb: list, top_k: int = 3):
    """
    質問の埋め込みに最も近い文章を検索
    """
    result = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    return result