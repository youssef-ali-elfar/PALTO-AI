# PALTO AI — Full-Stack MVP

This repository contains a working hackathon-oriented foundation for PALTO AI:

- Next.js frontend
- FastAPI backend
- Intent Router
- Short-term memory (last 10 messages)
- ChromaDB vector store
- Multilingual local embeddings
- RAG ingestion from official OpenFDA drug labeling
- Evidence/source metadata
- External LLM provider abstraction
- Fallback when the local knowledge base has insufficient evidence
- Safety validation
- Tests

## Security

The API key is loaded from `.env`. Never commit `.env`.

If a secret was ever pasted into chat, source code, screenshots, or GitHub, rotate it before use.

## Medical data

The ingestion script does not fabricate medical facts. It downloads public OpenFDA drug-label records and converts real label sections into RAG records.

Run:

```powershell
python scripts\ingest_openfda.py
```

This creates:

`data/processed/palto_medical_chunks.json`

and a persistent ChromaDB index.

The script is designed to produce 1000+ records when enough sectioned label data is returned.

OpenFDA documentation:
https://open.fda.gov/apis/drug/label/

OpenFDA warns that its API output should not be relied upon to make medical-care decisions. PALTO is a hackathon prototype, not a medical device.

## Backend

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python scripts\ingest_openfda.py
uvicorn backend.main:app --reload
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Then open the Next.js URL.

## Demo

Use a sequence such as:

1. "The patient is 55 years old."
2. "He has hypertension."
3. "He is taking sildenafil."
4. "Can he take nitrates?"
5. "What about if he took sildenafil 12 hours ago?"

The first three messages establish conversation memory. The clinical questions trigger retrieval and the evidence/safety pipeline.

## Architecture

Doctor -> Next.js -> FastAPI -> Intent Router -> Memory/RAG -> Vector DB -> LLM -> Safety -> Evidence -> UI
