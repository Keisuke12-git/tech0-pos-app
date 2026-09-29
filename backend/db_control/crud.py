from datetime import date, datetime
import json
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import TaxRates, Products, Transactions, TransactionDetails


#担当者IDとそのパスワードが一致する担当者の情報を取得して渡す
def mylogin(mymodel, staff_input_id, staff_input_password):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.staff_id == staff_input_id, mymodel.staff_password == staff_input_password)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.first() #resultはstaffsのクラス,一致がなければNoneが入る
            if result:
                result_staff_name = result.staff_name #staff_nameだけ取り出し
            else:
                result_staff_name = None
        
    except Exception as e:
        print(f"ログイン処理に失敗しました: {e}")

    # セッションを閉じる
    session.close()
    return result_staff_name

#今日時点で有効な税率を、税率マスタから取得する
def get_current_tax_rate():
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    today = date.today()
    query = (
        session.query(TaxRates)
        .filter(TaxRates.effective_date <= today)
        .order_by(TaxRates.effective_date.desc())
    )
    try:
        # トランザクションを開始
        with session.begin():
            result = query.first() #適用開始日が今日以前のものの中で、一番新しい1件
            if result:
                tax_rate = result.tax_rate
            else:
                tax_rate = None
    except Exception as e:
        print(f"税率取得に失敗しました: {e}")
        tax_rate = None
    session.close()
    return tax_rate


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
        tax_rate = get_current_tax_rate() #今日時点での税率を取得
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for product_info in result:
            if tax_rate is not None:
                price_incl_tax = int(product_info.price_excl_tax * (1 + tax_rate))
            else:
                price_incl_tax = None
            result_dict_list.append({
                "product_code": product_info.product_code,
                "product_name": product_info.product_name,
                "price_excl_tax": product_info.price_excl_tax,
                "price_incl_tax": price_incl_tax,
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except Exception as e:
        print(f"商品検索に失敗しました: {e}")

    # セッションを閉じる
    session.close()
    return result_json


#購入リストの中にある商品を購入確定して取引ヘッダへ保存する
def create_transaction(staff_id, member_id, product_codes):
    # session構築
    Session =sessionmaker(bind=engine)
    session = Session()

    new_transaction_id = None
    total_price_excl_tax = 0
    tax_amount = 0
    total_price_incl_tax = 0

    try:
        # トランザクションを開始（このsessionに対する最初のクエリをこの中に収めることで、
        # 「暗黙のトランザクションが先に始まってしまう」問題を避けている）
        with session.begin():
            transaction = {}
            tax_rate = get_current_tax_rate() #今日時点での税率を取得
            total_price_excl_tax = 0
            details_list = []

            for product_code in product_codes:
                product = session.query(Products).filter(Products.product_code == product_code).first()
                price_excl_tax = product.price_excl_tax
                total_price_excl_tax = total_price_excl_tax + price_excl_tax
                details_list.append({
                        "product_code": product.product_code,
                        "product_name": product.product_name,
                        "price_excl_tax": product.price_excl_tax,
                    })

            tax_amount = int(total_price_excl_tax * tax_rate)
            total_price_incl_tax = total_price_excl_tax + tax_amount

            transaction["transaction_datetime"] = datetime.now()
            transaction["staff_id"] = staff_id
            transaction["member_id"] = member_id
            transaction["tax_rate"] = tax_rate
            transaction["total_excl_tax"] = total_price_excl_tax
            transaction["tax_amount"] = tax_amount
            transaction["total_incl_tax"] = total_price_incl_tax

            query = insert(Transactions).values(**transaction)

            # データの挿入
            result = session.execute(query)
            new_transaction_id = result.inserted_primary_key[0]

            # 取引明細への保存
            transaction_detail = {}
            for index, detail in enumerate(details_list):
                transaction_detail["transaction_id"] = new_transaction_id
                transaction_detail["line_number"] = index
                transaction_detail["product_code"] = detail["product_code"]
                transaction_detail["product_name"] = detail["product_name"]
                transaction_detail["price_excl_tax"] = detail["price_excl_tax"]
                transaction_detail["quantity"] = 1
                transaction_detail["subtotal_excl_tax"] = detail["price_excl_tax"]

                query = insert(TransactionDetails).values(transaction_detail)
                result = session.execute(query)

    except Exception as e:
        print(f"取引の保存に失敗しました: {e}")
        new_transaction_id = None

    # セッションを閉じる
    session.close()

    if new_transaction_id is None:
        return None
    
    return {
        "transaction_id": new_transaction_id,
        "total_excl_tax": total_price_excl_tax,
        "tax_amount": tax_amount,
        "total_incl_tax": total_price_incl_tax,
    }

