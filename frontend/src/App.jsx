import { useState } from "react";
import "./style.css";

const API_URL = "http://127.0.0.1:5050/ask";

export default function App() {
  const [q, setQ] = useState("");
  const [history, setHistory] = useState([]);
  const [sessions, setSessions] = useState([{ session_id: "local", session_name: "名称未設定" }]);

  async function onSubmit(e) {
    e.preventDefault();
    const user = q.trim();
    if (!user) return;

    // まずユーザー発言だけ表示
    setHistory((h) => [...h, { user_input: user, answer: null }]);
    setQ("");

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q: user }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      // 直前のメッセージに回答を入れる
      setHistory((h) => {
        const copy = [...h];
        copy[copy.length - 1] = { ...copy[copy.length - 1], answer: data.answer };
        return copy;
      });
    } catch (err) {
      console.error("fetch failed:", err);
      setHistory((h) => {
        const copy = [...h];
        copy[copy.length - 1] = { ...copy[copy.length - 1], answer: "サーバーに接続できませんでした" };
        return copy;
      });
    }
  }

  function newSession() {
    setHistory([]);
  }
  function loadSession() {} // いまはダミー

  // ↓ ここからあなたの JSX（見た目）は今のままでOK
  return (
    <div className="container">
      <div className="sidebar">
        <h3>📅 過去の質問</h3>
        <ul style={{ padding: 0, margin: 0 }}>
          {sessions.map((s, idx) => (
            <li key={s.session_id} style={{ listStyle: "none", marginBottom: 10 }}>
              <button className="session-btn" onClick={() => loadSession(s.session_id)}>
                {idx + 1}: {s.session_name || "名称未設定"}
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className="main">
        <h1>ヴレインさん</h1>
        <img src="/nou.png" width="100" alt="bot" />
        <p>こんにちは！なにかご質問はありますか？🧠</p>

        <div className="chat-box chat-history">
          {history.map((h, i) => (
            <div key={i} className="chat-entry">
              <div className="chat-bubble user">{h.user_input}</div>
              {h.answer !== null && <div className="chat-bubble bot">{h.answer}</div>}
            </div>
          ))}
        </div>

        <form className="question-form" onSubmit={onSubmit}>
          <input
            name="user_input"
            placeholder="ご質問をどうぞ"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            required
          />
          <button type="submit" className="btn-success">送信</button>
        </form>

        <button className="new-session btn-success" style={{ marginTop: 12 }} onClick={newSession}>
          新しい質問を始める
        </button>
      </div>
    </div>
  );
}
