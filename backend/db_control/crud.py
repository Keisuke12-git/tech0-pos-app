import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine



#商品コードと一致する商品の情報を取得し、pythonで読み取れるjson形式にして渡す
def myselect(mymodel, product_code):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.product_code == product_code)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for product_info in result:
            result_dict_list.append({
                "product_code": product_info.product_code,
                "product_name": product_info.product_name,
                "price_excl_tax": product_info.price_excl_tax,
                #税込み価格も本来はここで表示させる、このときに税率マスタの連携が必要
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json