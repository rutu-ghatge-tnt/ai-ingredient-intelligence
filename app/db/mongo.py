# app/db/mongo.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# MongoDB client connection
client = AsyncIOMotorClient(settings.MONGO_URI)

# Reference to the main database
db = client[settings.MONGO_DB_NAME]

# Example access points to collections
branded_collection = db["branded_ingredients"]         # Holds branded ingredient definitions
inci_collection = db["inci_info"]                      # Optional: extra INCI metadata
graph_edges_collection = db["graph_edges"]             # Optional: precomputed graph relationships
