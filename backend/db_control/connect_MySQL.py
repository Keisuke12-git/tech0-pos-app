"""
Azure Database for MySQL への接続（engine）を組み立てるモジュール。
.env の値から接続文字列を作り、他のスクリプト（test_connection.py、
テーブル作成スクリプトなど）から import して使い回す。
"""

import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SSL_CA_PATH = os.getenv("SSL_CA_PATH")  # 未設定なら None のまま（まずはSSLなしで試す）

# ユーザー名・パスワードに @ & : / # などの記号が含まれていても接続文字列を壊さないよう、
# URLエンコードしてから埋め込む（quote_plus は "@" -> "%40" のように変換する）
# ※ DB_HOST/DB_PORTはDNS・数値の制約上こうした記号が入り得ないため対象外、
#   DB_NAMEはMySQL側の命名規則で危険な記号が使われる可能性が低いため対象外としている
DB_USER_ENCODED = quote_plus(DB_USER) if DB_USER else DB_USER
DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD) if DB_PASSWORD else DB_PASSWORD

DATABASE_URL = f"mysql+pymysql://{DB_USER_ENCODED}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

connect_args = {}
if SSL_CA_PATH:
    connect_args["ssl_ca"] = SSL_CA_PATH

engine = create_engine(DATABASE_URL, connect_args=connect_args)
