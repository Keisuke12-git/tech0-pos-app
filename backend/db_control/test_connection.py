"""
Azure Database for MySQL への接続確認用スクリプト。
実際の接続（engine）は db_control/connect_MySQL.py に集約し、ここでは
それを import して SELECT 1 が通るかを確認するだけにしている。

実行方法:
    python test_connection.py
"""

from sqlalchemy import text
from db_control.connect_MySQL import engine, DB_HOST, DB_PORT, DB_NAME, DB_USER

if __name__ == "__main__":
    print(f"接続先: {DB_HOST}:{DB_PORT} / DB名: {DB_NAME} / ユーザー: {DB_USER}")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("接続に成功しました。SELECT 1 の結果:", result.scalar())
    except Exception as e:
        print("接続に失敗しました。")
        print(f"エラーの型: {type(e).__name__}")
        print(f"エラー内容: {e}")
