from shoppingagent.db.client import db
from shoppingagent.db.schemas import Product, Review


def seed_products():
    products_collection = db["products"]
    products_collection.delete_many({})

    products = [
        Product(
            id=1,
            name="Organic Raw Honey",
            category="honey",
            price=14.99,
            description="Pure organic raw honey, unfiltered and cold-pressed",
            is_organic=True,
            reviews=[
                Review(rating=5.0, reviewer_name="Alice", review_text="Amazing honey! Best I've ever tried."),
                Review(rating=4.0, reviewer_name="Bob", review_text="Good quality, will buy again."),
            ],
            avg_rating=4.5,
        ),
        Product(
            id=2,
            name="Wildflower Honey",
            category="honey",
            price=12.99,
            description="Natural wildflower honey from local beekeepers",
            is_organic=False,
            reviews=[Review(rating=4.0, reviewer_name="Eve", review_text="Decent honey for the price.")],
            avg_rating=4.0,
        ),
        Product(
            id=3,
            name="Organic Manuka Honey",
            category="honey",
            price=29.99,
            description="Premium organic Manuka honey from New Zealand",
            is_organic=True,
            reviews=[Review(rating=5.0, reviewer_name="Henry", review_text="Worth every penny, incredible quality.")],
            avg_rating=5.0,
        ),
    ]

    # model_dump(by_alias=True) converts each Product back into a dict, using "_id" not "id"
    docs = [p.model_dump(by_alias=True) for p in products]
    products_collection.insert_many(docs)
    print(f"Inserted {len(docs)} validated products into '{products_collection.name}' collection.")


if __name__ == "__main__":
    seed_products()