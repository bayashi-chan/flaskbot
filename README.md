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
- CSS

## 実行環境について
-　

```bash
python app.py

## pythonファイルの補足
app.py …… 受付の人。Reactから質問を受け取って、search.pyに投げる。結果をLLMに投げる。返事をReactに返す。
search.py …… 資料室に検索依頼して、app.pyにデータを返している。
embed.py …… 文章を機械が読める形に変換する人。ベクトルに変換する作業
vector_store.py …… 資料室そのもの（ChromaDB）、ベクトルを保存する。

##　なぜbackendとragをフォルダで分けるのか。
分けないと、pyファイルがbackend直下に沢山できてしまい、どのpyファイルが役割ごちゃごちゃで入ってしまい、わかりにくい。
だからこそ、app.pyのAPI受付とragのAIの裏側処理を分けている。



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

gcloud CLI の環境って？
ざっくり言うと 「ターミナルから Google Cloud を操作できる道具が揃った状態
→googleアカウントにログインして、GCPを利用して発行されたプロジェクトIDとか使ったり、リージョン選択をする。
cd ~/Desktop/chatbot-portfolio
gcloud auth login　　　　　　　　　　　　　　　　　　 # これ打つと、ログインを要求される 
gcloud config set project <YOUR_PROJECT_ID>　　 # GCPのコンソールいって、発行されたIDを確かめる
gcloud config set run/region asia-northeast1   # 東京
npm i -g firebase-tools
firebase login

Firebase = GCP の“フロントエンド寄り”サービスセット
GCP = より汎用的・本格的なクラウド基盤

SQ Liteは、Cloud Run 上では保存が消える/不安定（再デプロイやスケールでファイル消失・インスタンスごとに別DB）なので、READMEに「デモ用・データは消えることがある
永続化したいなら Cloud SQL（Postgres or MySQL）へ移行すべし。