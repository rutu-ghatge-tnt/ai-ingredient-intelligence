# scripts/create_indexes.py

"""
Creates MongoDB indexes for faster matching queries.
Run this once after seeding your database.
"""

import asyncio
from app.db.collections import inci_col

async def main():
    # Create index on normalized INCI names
    await inci_col.create_index("inciName_normalized")
    print("Index created on inciName_normalized")

if __name__ == "__main__":
    asyncio.run(main())
