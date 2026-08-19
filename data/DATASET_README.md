# PALTO RAG Dataset

The dataset is generated from public regulatory drug-label data rather than fabricated medical facts.

Run:

`python scripts/ingest_openfda.py`

Output:

`data/processed/palto_medical_chunks.json`

Each record preserves:
- source
- source URL
- label ID
- drug name
- section
- chunk text

The same records are indexed into ChromaDB.

Official source:
https://open.fda.gov/apis/drug/label/
