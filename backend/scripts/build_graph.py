# scripts/build_graph.py

"""
One-off script to (re)build the graph cache at startup time if you want.
You can also just let the first predict call build it.
"""

import asyncio
from app.logic.graph_builder import build_graph

async def main():
    G = await build_graph(force=True)
    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

if __name__ == "__main__":
    asyncio.run(main())
