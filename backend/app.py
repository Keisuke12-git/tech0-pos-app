from fastapi import FastAPI, HTTPException, Response, Cookie, Depends
from fastapi.middleware.cors import CORSMiddleware
from db_control import crud, mymodels_MySQL
import json

from pydantic import BaseModel

import secrets

class StaffInput(BaseModel):
    input_staff_id: str
    input_staff_password: str

class TransactionInput(BaseModel):
    member_id: str | None = None
    items: list[str]

app = FastAPI()

session = {}

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#セッションを確認する
def verify_session(session_id: str = Cookie(None)):
    if session_id not in session:
        raise HTTPException(status_code=401, detail="ログインが必要です")
    return session[session_id]


#担当者マスタからIDとパスワードを検索して一致する担当者名を取得する
@app.post("/login")
def get_staff_name(staff_input: StaffInput, response: Response):
    result = crud.mylogin(mymodels_MySQL.Staffs, staff_input.input_staff_id, staff_input.input_staff_password)
    if result is None:
        raise HTTPException(status_code=401, detail="担当者IDまたはパスワードが正しくありません")
    session_id = secrets.token_hex(16)
    response.set_cookie(key="session_id", value=session_id) #ブラウザにCookieとして渡す
    session[session_id] = staff_input.input_staff_id #セッション対応表に書き込み
    return {"staff_name" : result}


#商品マスタから商品を検索して情報を取得する
@app.get("/products/{product_code}")
def read_one_product(product_code: str, staff_id: str = Depends(verify_session)):
    result = crud.myselect(mymodels_MySQL.Products, product_code)
    result_obj = json.loads(result)
    if not result_obj:
        raise HTTPException(status_code=404, detail="商品がマスタ未登録です")
    return result_obj[0]


#購入リストの中にある商品を購入確定して取引ヘッダへ保存する
@app.post("/transactions", status_code=201)
def create_transaction(transaction_input: TransactionInput, staff_id: str = Depends(verify_session)):
    result = crud.create_transaction(staff_id, transaction_input.member_id, transaction_input.items)
    if result is None:
        raise HTTPException(status_code=500, detail="購入処理に失敗しました。もう一度お試しください")
    return result