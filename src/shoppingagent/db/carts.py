from shoppingagent.db.client import db
from shoppingagent.db.products import search_products
from shoppingagent.db.schemas import Cart, CartItem

CART_ID = "main_cart"


def get_cart() -> Cart:
    """Fetches the current cart, creating an empty one if it doesn't exist yet."""
    carts_collection = db["carts"]
    doc = carts_collection.find_one({"_id": CART_ID})

    if doc is None:
        return Cart(id=CART_ID, items=[])

    return Cart(**doc)


def add_to_cart(product_id: int, quantity: int = 1) -> Cart:
    """
    Adds a product to the cart by product_id.
    If the product is already in the cart, increases its quantity instead of duplicating it.
    """
    carts_collection = db["carts"]

    # Look up product details directly (not via search) since we already know the exact ID
    products_collection = db["products"]
    product_doc = products_collection.find_one({"_id": product_id})

    if product_doc is None:
        raise ValueError(f"No product found with id {product_id}")

    cart = get_cart()

    # Check if this product is already in the cart
    existing_item = next((item for item in cart.items if item.product_id == product_id), None)

    if existing_item:
        existing_item.quantity += quantity
    else:
        cart.items.append(
            CartItem(
                product_id=product_id,
                name=product_doc["name"],
                price=product_doc["price"],
                quantity=quantity,
            )
        )

    # upsert=True means: update if it exists, insert if it doesn't — avoids a separate "does cart exist" check
    carts_collection.update_one(
        {"_id": CART_ID},
        {"$set": {"items": [item.model_dump() for item in cart.items]}},
        upsert=True,
    )

    return get_cart()


if __name__ == "__main__":
    add_to_cart(product_id=1, quantity=2)
    cart = get_cart()
    for item in cart.items:
        print(item.name, "-", item.quantity, "x", item.price)