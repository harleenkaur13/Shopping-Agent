from langchain.tools import tool
from shoppingagent.db.products import search_products
from shoppingagent.db.carts import add_to_cart as add_to_cart_db
from shoppingagent.db.orders import checkout as checkout_db


@tool
def search_products_tool(query: str) -> str:
    """
    Search the product catalog by name, category, or description.
    Use this when the user wants to find or browse products (e.g. "show me some honey").
    Returns a readable list of matching products with their id, name, price, and rating.
    """
    results = search_products(query)

    if not results:
        return f"No products found matching '{query}'."

    lines = [
        f"id={p.id} | {p.name} | ${p.price} | rating {p.avg_rating} | description: {p.description}"
        for p in results
    ]
    return "This is the complete and only information available for these products:\n" + "\n".join(lines)


@tool
def add_to_cart_tool(product_id: int, quantity: int = 1) -> str:
    """
    Add a specific product to the cart using its product_id.
    Use this only after you know the exact product_id (usually from a prior search).
    """
    try:
        cart = add_to_cart_db(product_id=product_id, quantity=quantity)
        return f"Added to cart. Cart now has {len(cart.items)} distinct item(s)."
    except ValueError as e:
        return f"Error: {e}"


@tool
def checkout_tool() -> str:
    """
    Complete the purchase for everything currently in the cart.
    Only use this when the user explicitly confirms they want to buy/checkout — never assume.
    """
    try:
        order = checkout_db()
        return f"Order placed successfully! Total: ${order.total}"
    except ValueError as e:
        return f"Error: {e}"