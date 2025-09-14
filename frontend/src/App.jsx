import { useEffect, useState } from "react";
const API = "http://127.0.0.1:6060";

const api = {
  async listSessions() {
    const r = await fetch(`${API}/api/sessions`);
    const d = await r.json();
    return d.items ?? d.list ?? d.sessions ?? d; // 互換
  },
  async createSession() {
    const r = await fetch(`${API}/api/sessions`, { method: "POST" });
    if (!r.ok) throw new Error(`createSession HTTP ${r.status}`);
    const d = await r.json();
    return { id: d.id, title: d.title ?? "名称未設定", last_ts: d.last_ts ?? "", turns: d.turns ?? 0 };
  },
  async renameSession(id, title) {
    const r = await fetch(`${API}/api/sessions/${id}/title`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    if (!r.ok) throw new Error(`rename HTTP ${r.status}`);
    return r.json();
  },
  async listMessages(id) {
    const r = await fetch(`${API}/api/sessions/${id}/messages`);
    const d = await r.json();
    return d.items ?? d.list ?? d.messages ?? d; // 互換
  },
  async sendMessage(id, content) {
    const r = await fetch(`${API}/api/sessions/${id}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }), // q でもOK（サーバ両対応）
    });
    if (!r.ok) throw new Error(`send HTTP ${r.status}`);
    const d = await r.json();
    const reply = d.reply ?? { role: "assistant", content: d.assistant, ts: d.timestamp };
    const message = d.message ?? { role: "user", content, ts: d.timestamp };
    return { message, reply };
  },
};

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [currentId, setCurrentId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // 初回ロード
  useEffect(() => {
    (async () => {
      const ss = await api.listSessions();
      setSessions(ss);
      if (ss.length > 0) setCurrentId(ss[0].id);
    })().catch(err => console.error("listSessions error", err));
  }, []);

  // セッション変更でログ読込
  useEffect(() => {
    if (!currentId) return;
    (async () => {
      const ms = await api.listMessages(currentId);
      setMessages(ms);
    })().catch(err => console.error("listMessages error", err));
  }, [currentId]);

  async function onNewSession() {
    try {
      const s = await api.createSession();
      setSessions(prev => [s, ...prev]);
      setCurrentId(s.id);
      setMessages([]);
    } catch (e) {
      console.error(e);
      alert("新規作成に失敗");
    }
  }

  async function onRename(id) {
    const cur = sessions.find(s => s.id === id);
    const name = window.prompt("新しいタイトル", cur?.title ?? "名称未設定");
    if (name == null) return;
    try {
      const { title } = await api.renameSession(id, name.trim() || "名称未設定");
      setSessions(prev => prev.map(s => (s.id === id ? { ...s, title } : s)));
    } catch (e) {
      console.error(e);
      alert("リネームに失敗");
    }
  }

  async function onSend() {
    const text = input.trim();
    if (!text || !currentId) return;
    setInput("");

    // 楽観表示（先に自分の発言を出す）
    const tmp = { role: "user", content: text, ts: new Date().toISOString().slice(0,19).replace("T"," ") };
    setMessages(prev => [...prev, tmp]);

    try {
      const { message, reply } = await api.sendMessage(currentId, text);
      // 重複を避けつつ返信を追加
      setMessages(prev => [...prev, reply]);
      // 左リストの更新
      setSessions(prev =>
        prev.map(s => (s.id === currentId ? { ...s, last_ts: reply?.ts ?? tmp.ts, turns: (s.turns ?? 0) + 1 } : s))
      );
    } catch (e) {
      console.error(e);
      alert("送信に失敗");
    }
  }

  // デバッグ: クリックが実行されているか
  useEffect(() => {
    window.__debug = { sessions, currentId, messages };
  }, [sessions, currentId, messages]);

  return (
    <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", height: "100vh", gap: "16px", padding: 16, background: "#f5f7fa" }}>
      {/* 左ペイン */}
      <aside style={{ background: "white", borderRadius: 12, padding: 12, overflowY: "auto", boxShadow: "0 2px 10px rgba(0,0,0,.06)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <b>過去の質問</b>
          <button onClick={onNewSession} style={btnSm} data-testid="btn-new">+ 新しい質問</button>
        </div>
        {sessions.length === 0 && <div style={{ color: "#888", fontSize: 14 }}>まだありません</div>}
        {sessions.map(s => (
          <div
            key={s.id}
            onClick={() => setCurrentId(s.id)}
            onDoubleClick={() => onRename(s.id)}
            style={{
              padding: "8px 10px",
              borderRadius: 8,
              cursor: "pointer",
              background: s.id === currentId ? "#e8f5ee" : "transparent",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 6,
            }}
            title="ダブルクリックで名前変更"
          >
            <span style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {s.title || "名称未設定"}
            </span>
            <span style={{ color: "#999", fontSize: 12 }}>{s.turns ?? 0}</span>
          </div>
        ))}
      </aside>

      {/* 右ペイン */}
      <main style={{ background: "white", borderRadius: 12, padding: 24, display: "flex", flexDirection: "column", boxShadow: "0 2px 10px rgba(0,0,0,.06)" }}>
        <h1 style={{ marginTop: 0, marginBottom: 8 }}>ヴレインさん</h1>

        <div style={{ flex: 1, overflowY: "auto", border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
          {currentId ? (
            messages.length === 0 ? (
              <div style={{ color: "#888" }}>こんにちは！なにかご質問はありますか？ 🧠</div>
            ) : (
              messages.map((m, i) => (
                <div key={i} style={{ margin: "8px 0", textAlign: m.role === "user" ? "right" : "left" }}>
                  <div style={{
                    display: "inline-block",
                    background: m.role === "user" ? "#e6f3ff" : "#f2f2f2",
                    padding: "8px 10px",
                    borderRadius: 8,
                    maxWidth: "70%"
                  }}>
                    <div style={{ fontSize: 12, color: "#888", marginBottom: 4 }}>{m.role}</div>
                    <div>{m.content}</div>
                  </div>
                </div>
              ))
            )
          ) : (
            <div style={{ color: "#888" }}>左の「新しい質問」を押して始めよう！</div>
          )}
        </div>

        <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && onSend()}
            placeholder="あ…"
            style={{ flex: 1, padding: "10px 12px", borderRadius: 8, border: "1px solid #ddd" }}
          />
          <button onClick={onSend} style={btnLg} data-testid="btn-send">送信</button>
        </div>
      </main>
    </div>
  );
}

const btnSm = { padding: "6px 10px", borderRadius: 8, border: "none", background: "#28a745", color: "white", cursor: "pointer" };
const btnLg = { padding: "10px 16px", borderRadius: 10, border: "none", background: "#28a745", color: "white", fontWeight: 700, cursor: "pointer" };
