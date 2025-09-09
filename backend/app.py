# backend/app.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "your_secret_key"
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # 開発中

DB = Path(__file__).with_name("questions.db")

def get_conn():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON;")
    return con

def init_db():
    with get_conn() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            answer TEXT,
            timestamp TEXT,
            session_id TEXT,
            session_name TEXT
        );
        """)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    q = (data.get("q") or "").strip()
    if not q:
        return jsonify(ok=False, answer="質問が空だよ〜"), 400

    # セッションID（簡易）
    sid = session.get("session_id")
    if not sid:
        sid = str(datetime.now().timestamp())
        session["session_id"] = sid

    answer = f"（仮）あなたの質問: {q}"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_conn() as con:
        con.execute(
            "INSERT INTO questions (user_input, answer, timestamp, session_id) VALUES (?,?,?,?)",
            (q, answer, ts, sid),
        )

    return jsonify(ok=True, answer=answer)


# 必要なら履歴削除API（任意）
@app.route("/delete_history", methods=["POST"])
def delete_history():
    sid = session.get("session_id")
    if sid:
        with get_conn() as con:
            con.execute("DELETE FROM questions WHERE session_id = ?", (sid,))
    return jsonify(ok=True)

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5050, debug=True)
