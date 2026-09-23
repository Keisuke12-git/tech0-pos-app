# 簡易POSアプリ 実行手順（POS-main）

Windows 11 / PowerShell を前提とした手順です。

## backend（FastAPI）

DB関連のスクリプト（接続・テーブル定義・テーブル作成）は`db_control/`にまとめています。

```powershell
# 1. backendフォルダへ移動
cd backend

# 2. 仮想環境を作成（初回のみ）
python -m venv backend_env

# 3. 仮想環境を有効化
.\backend_env\Scripts\activate.ps1

# 4. 必要なパッケージをインストール（初回のみ・パッケージが増えたら都度）
pip install python-dotenv sqlalchemy pymysql

# 5. .env を確認する
#    DB_USER / DB_PASSWORD / DB_HOST / DB_PORT / DB_NAME を、
#    値に # やスペースが含まれる場合は "" で囲んで設定しておくこと

# 6. DB接続確認を実行
#    db_control/ 配下のスクリプトは、backendフォルダにいる状態で
#    「-m db_control.ファイル名」の形（モジュールとして）で実行する
#    （直接 python db_control/test_connection.py のように実行すると
#      db_controlパッケージが見つからずエラーになる）
python -m db_control.test_connection

# 7. テーブルを作成する（mymodels_MySQL.py の定義をDBに反映する）
python -m db_control.create_tables_MySQL
```

仮想環境を抜けるときは `deactivate` を実行する。

PowerShellでアクティベートスクリプトの実行がブロックされる場合は、実行ポリシーの制限が原因のことがある（その場合は個別に対処する）。

今後、`app.py`（FastAPIアプリ本体）ができたら、以下で起動する。

```powershell
uvicorn app:app --reload
# ブロックされる場合
python -m uvicorn app:app --reload
```

## frontend（Next.js）

まだ着手前。着手時は、サンプル（`LinkFastAPINext_Practical-main/frontend`）と同様の流れになる見込み。

```powershell
# 1. frontendフォルダへ移動
cd frontend

# 2. 依存パッケージをインストール（初回のみ）
npm install

# 3. .env にAPIエンドポイント（backendのURL）を設定する
#    例: NEXT_PUBLIC_API_ENDPOINT="http://localhost:8000"

# 4. 開発サーバーを起動
npm run dev
```

`http://localhost:3000` でアクセスできる想定。
