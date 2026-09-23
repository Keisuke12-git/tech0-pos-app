from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_control import crud, mymodels_MySQL
import json

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#商品マスタから商品を検索して情報を取得する
@app.get("/products/{product_code}")
def read_one_product(product_code: str):
    result = crud.myselect(mymodels_MySQL.Products, product_code)
    result_obj = json.loads(result)
    if not result_obj:
        raise HTTPException(status_code=404, detail="商品がマスタ未登録です")
    return result_obj[0]