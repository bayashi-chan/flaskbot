from flask import Flask,render_template,request
import sqlite3 

app = Flask(__name__)

# 初期化：テーブルがなければ作成
def init_db():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]

    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("INSERT INTO questions (content) VALUES (?)", (user_input,))
    conn.commit()
    conn.close()
    
    return f"あなたの質問：{user_input} に対しての回答です。"

if __name__ == '__main__':
    init_db()  # ← アプリ起動時にDB初期化
    app.run(debug=True)

