import asyncio
from app.logic.matcher import match_inci_names  

async def test_match():
    matched, unmatched = await match_inci_names([
        "Acetyl Hexapeptide-8",
        "Quaternium-73",
        "Copernicia Cerifera (Carnauba) Wax"
    ])
    print("Matched:", matched)
    print("Unmatched:", unmatched)

asyncio.run(test_match())
