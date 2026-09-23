"use client";
import { useState, useRef } from "react";

import fetchProduct from "./fetchProduct";

export default function OrderPage() {
    const inputRef = useRef();
    const [orderProducts, setOrderProducts] = useState([]);
    const counterRef = useRef(0);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const product_code = inputRef.current.value;
        const new_order = await fetchProduct(product_code);
        counterRef.current = counterRef.current +1;
        const orderedProduct = {...new_order, order_id : counterRef.current};
        console.log(orderedProduct); //検証用コンソール確認コード
        setOrderProducts([...orderProducts, orderedProduct]);
    };

    console.log(orderProducts); //検証用コンソール確認コード

    return (
        <>
            {/* form画面作成 */}
            <form onSubmit = {handleSubmit}>
                <p>
                    商品コード：
                    <input ref = {inputRef} />
                </p>
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
                            税抜価格： {orderProduct.price_excl_tax}
                        </p>
                    </div>
                ))}
            </div>
        </>
    )
}