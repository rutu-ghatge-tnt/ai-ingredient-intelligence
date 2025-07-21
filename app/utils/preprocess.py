# app/utils/preprocess.py

import re

def normalize_inci_list(inci_list: list[str]) -> list[str]:
    """
    Normalize INCI names: trim, title-case, remove duplicates.
    Input: ["glycerin ", " aqua", "TOCOPHERYL acetate"]
    Output: ["Glycerin", "Aqua", "Tocopheryl Acetate"]
    """
    seen = set()
    cleaned = []

    for raw in inci_list:
        name = re.sub(r'\s+', ' ', raw.strip()).title()
        if name not in seen:
            seen.add(name)
            cleaned.append(name)

    return cleaned
