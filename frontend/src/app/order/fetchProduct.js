export default async function fetchProduct(product_code) {
    const res = await fetch(
        process.env.NEXT_PUBLIC_API_ENDPOINT + `/products/${product_code}`,
        { cache: "no-cache", credentials: "include" }
    );
    if (!res.ok) {
        throw new Error("Failed to fetch product");
    }
    return res.json();
}