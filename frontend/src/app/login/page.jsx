"use client";
import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import fetchStaff from "./fetchStaff";

export default function LoginPage() {
    const inputIDRef = useRef();
    const inputPasswordRef = useRef();
    const router = useRouter();
    const [errorMessage, setErrorMessage] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const input_staff_id = inputIDRef.current.value;
            const input_staff_password = inputPasswordRef.current.value;
            const logined_staff_name = await fetchStaff(input_staff_id, input_staff_password);
            router.push(`/order?staff_name=${logined_staff_name.staff_name}`);
        } catch (error) {
            setErrorMessage(error.message);
        }
    };

    return (
        <>
            {/* form画面作成 */}
            <form onSubmit = {handleSubmit}>
                <p>
                    担当者ID:
                    <input ref = {inputIDRef} />
                </p>
                <p>
                    パスワード:
                    <input
                        type="password"
                        ref = {inputPasswordRef}
                    />
                </p>
                <button type="submit">ログイン</button>
                {errorMessage && <p>{errorMessage}</p>}
            </form>
        </>
    )

}