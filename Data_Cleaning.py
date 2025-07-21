import json
import re

def clean_key(key):
    """Remove trailing spaces and convert to snake_case."""
    return re.sub(r'\s+', '_', key.strip().lower())

def convert_str_list(value):
    """Convert stringified list to actual list if it's a JSON list."""
    if isinstance(value, str) and value.strip().startswith("[") and value.strip().endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [value.strip()]  # fallback as single item list
    return value

def clean_value(value):
    """Clean individual field value."""
    if isinstance(value, str):
        value = value.strip()
        return value if value else None
    if isinstance(value, list):
        value = [v.strip() if isinstance(v, str) else v for v in value]
        return value if value else None
    return value

def clean_entry(entry):
    """Clean a single JSON record."""
    cleaned = {}
    for key, value in entry.items():
        clean_k = clean_key(key)
        value = convert_str_list(value)
        clean_v = clean_value(value)
        cleaned[clean_k] = clean_v
    return cleaned

def clean_json_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_data = []
    for line in lines:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            cleaned_entry = clean_entry(entry)
            cleaned_data.append(cleaned_entry)
        except json.JSONDecodeError:
            print("⚠️ Skipping bad line:", line[:80])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Cleaned data written to: {output_path}")

# Example usage
clean_json_file(
    input_path="202507161239-skinbb_prospector_cosmetics_pdfextraction_20250716.json",
    output_path="cleaned_skinbb_prospector_short.json"
)
