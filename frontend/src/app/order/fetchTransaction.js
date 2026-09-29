export default async function fetchTransaction(member_id, items) {
    const res = await fetch(
        process.env.NEXT_PUBLIC_API_ENDPOINT + `/transactions`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                member_id: member_id,
                items: items,
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