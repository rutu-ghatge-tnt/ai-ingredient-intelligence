# app/utils/graph.py

import networkx as nx

def build_ingredient_graph(inci_list: list[str], matched_brands: list[dict]) -> float:
    """
    Use NetworkX to create an ingredient co-occurrence graph from input INCI list and
    matched branded ingredients, then compute a graph-based confidence multiplier.

    Returns a float multiplier between 0.7 and 1.0, higher means stronger ingredient linkage.
    """
    G = nx.Graph()

    # Add nodes for each INCI
    for inci in inci_list:
        G.add_node(inci)

    # Add edges between INCI that belong to same branded ingredient
    for brand in matched_brands:
        inc_set = brand.matched_inci
        # Fully connect all matched INCI of this brand (clique)
        for i in range(len(inc_set)):
            for j in range(i + 1, len(inc_set)):
                G.add_edge(inc_set[i], inc_set[j])

    # Calculate graph density (ratio of actual edges to possible edges)
    density = nx.density(G)
    # Normalize density to multiplier scale
    multiplier = 0.7 + (density * 0.3)
    return round(min(max(multiplier, 0.7), 1.0), 3)
