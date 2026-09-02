from shoppingagent.db.client import db
from shoppingagent.db.schemas import Product


def search_products(query: str, sort_by: str = "avg_rating"):
    """
    Searches products by matching the query text against name, category, or description.
    Returns a list of validated Product objects, sorted by highest rating first by default.
    """
    products_collection = db["products"]

    filter_query = {
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
        ]
    }

    raw_results = products_collection.find(filter_query).sort(sort_by, -1)

    # Convert each raw Mongo dict into a validated Product object
    return [Product(**doc) for doc in raw_results]


if __name__ == "__main__":
    results = search_products("honey")
    for product in results:
        print(product.name, "-", product.price, "-", product.avg_rating)