from flask import Flask,render_template,request,redirect,url_for
import sqlite3 

app = Flask(__name__)

# 初期化：テーブルがなければ作成
def init_db():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    answer TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    # DB kara kaiwa rireki wo syutoku
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("SELECT user_input, answer FROM questions")
    history = c.fetchall()
    conn.close()
    
    return render_template("index.html", history=history)


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    
    # 仮の回答（ここにGPT連携とか入れてもOK）
    answer = f"{user_input} に対しての回答です。"


    # DBに保存
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("INSERT INTO questions (user_input, answer) VALUES (?, ?)", (user_input, answer))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))  # "/"に戻ってチャット履歴を表示

if __name__ == '__main__':
    init_db()  # ← アプリ起動時にDB初期化
    app.run(host='0.0.0.0', port=5001, debug=True)

