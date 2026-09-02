from shoppingagent.db.client import db
from shoppingagent.db.carts import get_cart, CART_ID
from shoppingagent.db.schemas import Order


def checkout() -> Order:
    """
    Converts the current cart into an order, then empties the cart.
    Raises an error if the cart is empty.
    """
    cart = get_cart()

    if not cart.items:
        raise ValueError("Cannot checkout — cart is empty")

    total = sum(item.price * item.quantity for item in cart.items)

    order = Order(items=cart.items, total=round(total, 2))

    orders_collection = db["orders"]
    result = orders_collection.insert_one(order.model_dump(by_alias=True, exclude={"id"}))

    # Empty the cart now that checkout is complete
    carts_collection = db["carts"]
    carts_collection.update_one({"_id": CART_ID}, {"$set": {"items": []}})

    order.id = str(result.inserted_id)
    return order


if __name__ == "__main__":
    completed_order = checkout()
    print(f"Order placed! Total: ${completed_order.total}")
    for item in completed_order.items:
        print(" -", item.name, "x", item.quantity)