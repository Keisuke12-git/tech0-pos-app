"""
mymodels_MySQL.py で定義したテーブルを、connect_MySQL.py の接続先
（.env の DB_NAME で指定したデータベース）に実際に作成するスクリプト。

実行方法:
    python create_tables_MySQL.py
"""

from db_control.mymodels_MySQL import Base
from db_control.connect_MySQL import engine

if __name__ == "__main__":
    print("テーブルを作成しています >>>")
    Base.metadata.create_all(bind=engine)
    print("完了しました。")
