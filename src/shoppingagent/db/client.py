from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Loads variables from .env into the environment, so we can read them with os.getenv()
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "shoppingagent"

# One shared client for the whole app — created once, reused everywhere
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]