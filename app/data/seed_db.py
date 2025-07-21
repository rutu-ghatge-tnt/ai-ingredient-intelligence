# app/data/seed_db.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Load JSON seed files
BRANDED_PATH = "app/data/branded_ingredients_seed.json"
INCI_PATH = "app/data/inci_info_seed.json"

async def seed_database():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    
    branded_collection = db["branded_ingredients"]
    inci_collection = db["inci_info"]

    # Clear existing data (optional)
    await branded_collection.delete_many({})
    await inci_collection.delete_many({})

    # Load branded ingredients
    with open(BRANDED_PATH, "r", encoding="utf-8") as f:
        branded_data = json.load(f)
        await branded_collection.insert_many(branded_data)

    # Load INCI metadata
    with open(INCI_PATH, "r", encoding="utf-8") as f:
        inci_data = json.load(f)
        await inci_collection.insert_many(inci_data)

    print("✅ MongoDB seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_database())
