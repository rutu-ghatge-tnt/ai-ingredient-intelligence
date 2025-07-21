# app/utils/scoring.py

from app.models.schemas import BrandedIngredient, Conflict


def score_matches(cleaned_inci: list[str], branded_data: list[dict]) -> tuple[list[BrandedIngredient], list[Conflict], list[str]]:
    matched = []
    unmatched_set = set(cleaned_inci)
    conflicts = []
    inci_to_brands = {}

    # Map INCI → possible product names (not brand_name)
    for brand in branded_data:
        product_name = brand.get("product_name", "Unknown")  # ✅ updated
        for inci in brand["inci_names"]:
            inci_to_brands.setdefault(inci, set()).add(product_name)  # ✅ updated

    # Subset-based match
    for brand in branded_data:
        brand_inci = set(brand["inci_names"])
        if brand_inci.issubset(set(cleaned_inci)):
            proximity_score = _calculate_proximity(cleaned_inci, list(brand_inci))
            common_factor = _rarity_boost(brand_inci, branded_data)
            confidence = round(proximity_score * common_factor, 3)

            matched.append(BrandedIngredient(
                product_name=brand.get("product_name", "Unknown"),
                supplier=brand.get("company_name", "Unknown"),
                matched_inci=list(brand_inci),
                confidence_score=confidence,
                description=brand.get("description"),
                documentation_url=brand.get("documents", [None])[0],  # Use first document if available
                functionality_category=None,
                chemical_class_category=None
            ))
          

            unmatched_set -= brand_inci

    # Conflict logic
    for inci in cleaned_inci:
        possible = inci_to_brands.get(inci, [])
        if len(possible) > 1:
            conflicts.append(Conflict(
                inci_name=inci,
                possible_brands=list(possible),
                context="Ingredient used in multiple branded complexes"
            ))

    return matched, conflicts, list(unmatched_set)



def _calculate_proximity(inci_list: list[str], brand_incis: list[str]) -> float:
    """
    Score how close brand INCI components are within the user list.
    Closer = higher confidence.
    """
    indices = [inci_list.index(i) for i in brand_incis if i in inci_list]
    if not indices or len(indices) == 1:
        return 0.6
    spread = max(indices) - min(indices)
    return round(1.0 - (spread / len(inci_list)), 3)


def _rarity_boost(inci_set: set, branded_data: list[dict]) -> float:
    generic = {"Aqua", "Water", "Glycerin", "Fragrance", "Alcohol", "Phenoxyethanol"}
    if inci_set & generic:
        return 0.85
    return 1.0
