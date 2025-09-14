from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)  # 開発中は全許可にして詰まりを避ける

DB = Path(__file__).with_name("questions.db")

def get_conn():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON;")
    return con

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def new_sid():
    return str(int(datetime.now().timestamp() * 1000))

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

@app.get("/health")
def health():
    return jsonify(ok=True, ts=now_str()), 200

@app.get("/__routes")
def routes():
    return jsonify(sorted(r.rule for r in app.url_map.iter_rules() if "static" not in r.rule)), 200

@app.get("/api/sessions")
def list_sessions():
    with get_conn() as con:
        cur = con.execute("""
            SELECT
                session_id AS id,
                COALESCE(NULLIF(MAX(session_name), ''), '名称未設定') AS title,
                MAX(timestamp) AS last_ts,
                COUNT(CASE WHEN user_input IS NOT NULL AND user_input<>'' THEN 1 END) AS turns
            FROM questions
            GROUP BY session_id
            ORDER BY last_ts DESC
        """)
        items = [dict(r) for r in cur.fetchall()]
    return jsonify({"items": items}), 200

@app.post("/api/sessions")
def create_session():
    sid, ts = new_sid(), now_str()
    with get_conn() as con:
        con.execute("INSERT INTO questions(session_id, session_name, timestamp) VALUES(?,?,?)",
                    (sid, "名称未設定", ts))
    return jsonify({"id": sid, "title": "名称未設定", "last_ts": ts, "turns": 0}), 201

@app.patch("/api/sessions/<sid>/title")
def rename_session(sid):
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip() or "名称未設定"
    with get_conn() as con:
        con.execute("UPDATE questions SET session_name=? WHERE session_id=?", (title, sid))
    return jsonify({"id": sid, "title": title}), 200

@app.get("/api/sessions/<sid>/messages")
def get_messages(sid):
    with get_conn() as con:
        cur = con.execute("SELECT user_input, answer, timestamp FROM questions WHERE session_id=? ORDER BY id", (sid,))
        msgs = []
        for row in cur.fetchall():
            if row["user_input"]:
                msgs.append({"role": "user", "content": row["user_input"], "ts": row["timestamp"]})
            if row["answer"]:
                msgs.append({"role": "assistant", "content": row["answer"], "ts": row["timestamp"]})
    return jsonify(msgs), 200

@app.post("/api/sessions/<sid>/messages")
def add_message(sid):
    data = request.get_json(silent=True) or {}
    q = (data.get("content") or data.get("q") or "").strip()
    if not q:
        return jsonify(ok=False, error="content required"), 400
    ans, ts = f"（仮）あなたの質問: {q}", now_str()
    with get_conn() as con:
        con.execute("INSERT INTO questions (user_input, answer, timestamp, session_id) VALUES (?,?,?,?)",
                    (q, ans, ts, sid))
    return jsonify(ok=True, session_id=sid,
                message={"role": "user", "content": q, "ts": ts},
                reply={"role": "assistant", "content": ans, "ts": ts}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=6060, debug=True, use_reloader=False)
