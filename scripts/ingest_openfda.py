import json
import os
from pathlib import Path
import requests
from backend.rag.vector_store import vector_store

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "openfda_labels.json"
OUT = ROOT / "data" / "processed" / "palto_medical_chunks.json"
URL = "https://api.fda.gov/drug/label.json"

SECTION_FIELDS = [
    "boxed_warning",
    "warnings",
    "warnings_and_precautions",
    "contraindications",
    "indications_and_usage",
    "dosage_and_administration",
    "adverse_reactions",
    "drug_interactions",
    "use_in_specific_populations",
    "overdosage",
    "clinical_pharmacology",
    "description",
]

def flatten(value):
    if isinstance(value, list):
        return "\n".join(str(x) for x in value)
    return str(value)

def main():
    limit = min(int(os.getenv("OPENFDA_LIMIT", "1000")), 1000)
    response = requests.get(URL, params={"limit": limit}, timeout=120)
    response.raise_for_status()
    data = response.json()

    RAW.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    records = []

    for idx, item in enumerate(data.get("results", [])):
        openfda = item.get("openfda", {})
        generic = flatten(openfda.get("generic_name", ["Unknown"]))
        brand = flatten(openfda.get("brand_name", ["Unknown"]))
        title = f"{generic} ({brand})"
        label_id = item.get("id") or item.get("set_id") or f"label-{idx}"
        source_url = (
            "https://open.fda.gov/apis/drug/label/?search=id:"
            + str(label_id)
        )

        for field in SECTION_FIELDS:
            raw = item.get(field)
            if not raw:
                continue

            text = flatten(raw).strip()
            if len(text) < 80:
                continue

            max_chars = 3500
            for part in range(0, len(text), max_chars):
                chunk = text[part:part + max_chars].strip()
                if len(chunk) < 80:
                    continue

                records.append({
                    "id": f"{label_id}-{field}-{part // max_chars}",
                    "text": chunk,
                    "title": title,
                    "section": field,
                    "source": "OpenFDA / FDA Structured Product Labeling",
                    "source_url": source_url,
                    "label_id": str(label_id),
                    "generic_name": generic,
                    "brand_name": brand,
                })

    OUT.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Created {len(records)} RAG records.")
    print(f"JSON: {OUT}")

    for i in range(0, len(records), 64):
        vector_store.add_documents(records[i:i + 64])
        print(f"Indexed {min(i + 64, len(records))}/{len(records)}")

if __name__ == "__main__":
    main()
