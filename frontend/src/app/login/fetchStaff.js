export default async function fetchStaff(input_staff_id, input_staff_password) {
    const res = await fetch(
        process.env.NEXT_PUBLIC_API_ENDPOINT + `/login`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" }, //今から送るのはjson形式だと明示
            body: JSON.stringify({
                input_staff_id: input_staff_id,
                input_staff_password: input_staff_password,
            }),
            cache: "no-cache",
            credentials: "include",
        }
    );
    if (!res.ok) {
        const errorBody = await res.json();
        throw new Error(errorBody.detail);
    }
    return res.json();
}