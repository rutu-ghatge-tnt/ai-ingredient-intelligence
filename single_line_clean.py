import json
import pandas as pd

def flatten_and_clean(entry):
    cleaned = {}
    for k, v in entry.items():
        if isinstance(v, list):
            cleaned[k] = ' | '.join(v) if v else None
        elif isinstance(v, str) and v.strip() == "":
            cleaned[k] = None
        else:
            cleaned[k] = v
    return cleaned

# Load cleaned JSON
with open("cleaned_skinbb_prospector.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Clean and flatten each record
flattened_data = [flatten_and_clean(entry) for entry in data]

# Convert to DataFrame
df = pd.DataFrame(flattened_data)

# Save to Excel
df.to_excel("skinbb_prospector_cleaned_flat.xlsx", index=False)

print("✅ Exported with lists flattened and empty fields set to null.")
