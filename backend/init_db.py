# init_db.py
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("questions.db")

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    # 就業規則などの本文
    cur.execute("""
        CREATE TABLE IF NOT EXISTS docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            content TEXT NOT NULL
        );
    """)

    # （任意）問い合わせログ
    cur.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            q_text   TEXT NOT NULL,
            created  TEXT DEFAULT (datetime('now','localtime'))
        );
    """)

    # サンプル投入（既存がなければ）
    cur.execute("SELECT COUNT(*) FROM docs;")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO docs(title, content) VALUES(?, ?);",
            [
                ("就業時間", "所定労働時間は9:00〜18:00（休憩60分）。"),
                ("有給休暇", "入社半年後に10日付与。以後、勤続年数に応じ付与。"),
                ("残業・申請", "残業は事前申請が原則。36協定の範囲内で運用。"),
            ],
        )

    con.commit()
    con.close()
    print("OK: DB初期化完了 -> questions.db")

if __name__ == "__main__":
    init_db()
