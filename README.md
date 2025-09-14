# FlaskBot
簡単なFlaskアプリです。質問を入力すると、回答を返します。  
入力内容はSQLiteのデータベースに保存されます。


## 特徴
- 質問をデータベースに保存
- 回答を画面に表示

## 使用技術
- Python
- Flask
- SQLite3
- HTML/CSS

## 実行方法（ローカル）

```bash
python app.py



VSCode の「Git: Untracked Changes = hidden」とは別物。
.gitignore → Git 側で無視する（表示されない）
hidden → VSCode 側で非表示にするだけ
ただし、.gitignore が効くのは まだ Git に追加してないファイルだけ。すでに git add やコミットしてるものは、.gitignore に書いても消えない
→ その場合は git rm --cached ファイル名 で「追跡解除」する必要あり。


フロント(5173)とAPI(6060)は別オリジンだから、普通に叩くとCORSで怒られる。
proxyを使えば“5173に向けて相対パスで呼んだ”ことになり、CORS問題を回避できる。
まず登場人物
フロント＝見た目担当のお店 … localhost:5173
API＝裏方のキッチン … localhost:6060
CORS＝お店の警備員。「同じ建物の人だけ通していいよ」と見張ってる
proxy（プロキシ）＝フロントとキッチンをつなぐ裏口トンネル