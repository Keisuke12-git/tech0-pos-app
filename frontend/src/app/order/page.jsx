"use client";
import { useState, useRef } from "react";
import { useSearchParams } from "next/navigation";

import fetchProduct from "./fetchProduct";
import fetchTransaction from "./fetchTransaction";

export default function OrderPage() {
    const inputRef = useRef();
    const [orderProducts, setOrderProducts] = useState([]);
    const counterRef = useRef(0);
    const searchParams = useSearchParams();
    const staff_name = searchParams.get("staff_name");
    const [transactionResult, setTransactionResult] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const product_code = inputRef.current.value;
        const new_order = await fetchProduct(product_code);
        counterRef.current = counterRef.current +1;
        const orderedProduct = {...new_order, order_id : counterRef.current};
        console.log(orderedProduct); //検証用コンソール確認コード
        setOrderProducts([...orderProducts, orderedProduct]);
    };

    const handlePurchase = async (event) => {
        event.preventDefault();
        const items = orderProducts.map((orderProduct) => orderProduct.product_code);
        const transaction_result = await fetchTransaction(null, items); //会員ログインを実装したらmember_idを渡せるように
        setTransactionResult(transaction_result)
    };

    console.log(orderProducts); //検証用コンソール確認コード

    return (
        <>
            <p>担当者：{staff_name}</p>
            {/* form画面作成 */}
            <form onSubmit = {handleSubmit}>
                <p>
                    商品コード：
                    <input ref = {inputRef} />
                </p>
                <button>
                    登録
                </button>
            </form>

            {/* 購入リスト画面作成 */}
            <div>
                購入リスト
                {orderProducts.map((orderProduct) => (
                    <div
                        key = {orderProduct.order_id}>
                        <p>
                            商品名： {orderProduct.product_name}
                        </p>
                        <p>
                            価格： {orderProduct.price_excl_tax}円（税込{orderProduct.price_incl_tax}円）
                        </p>
                    </div>
                ))}
            </div>

            {/* 購入確定ボタン */}
            <button onClick = {handlePurchase}>
                購入確定ボタン
            </button>

            {/* 購入確定後ポップアップ表示 */}
            {transactionResult && (
            <div>
                <p>購入完了しました</p>
                <p>合計金額（税込）：{transactionResult.total_incl_tax}円</p>
                <p>合計金額（税抜）：{transactionResult.total_excl_tax}円</p>
            </div>
            )}

        </>
    )
}