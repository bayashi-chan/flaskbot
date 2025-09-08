from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理のために必要！

DB_NAME = "questions.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            answer TEXT,
            timestamp TEXT,
            session_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(datetime.now().timestamp())
        session['session_id'] = session_id

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT user_input, answer FROM questions WHERE session_id = ?", (session_id,))
    history = c.fetchall()

    c.execute("SELECT DISTINCT session_id FROM questions ORDER BY id DESC")
    sessions = c.fetchall()
    conn.close()

    return render_template("index.html", history=history, sessions=sessions, current_session=session_id)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    # 仮の回答（ここにGPT連携とか入れてもOK）
    answer = f"{user_input} に対しての回答です。"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = session.get("session_id")

    # DBに保存
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("INSERT INTO questions (user_input, answer, timestamp, session_id) VALUES (?, ?, ?, ?)",
                (user_input, answer, timestamp, session_id))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/session/<sid>")
def load_session(sid):
    session['session_id'] = sid
    return redirect(url_for("index"))

@app.route('/new_session', methods=['POST'])
def new_session():
    session.pop('session_id', None)
    return redirect(url_for('index'))

@app.route('/delete_history', methods=['POST'])
def delete_history():
    sid = session.get("session_id")
    if sid:
        conn = get_db_connection()
        conn.execute("DELETE FROM questions WHERE session_id = ?", (sid,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)

