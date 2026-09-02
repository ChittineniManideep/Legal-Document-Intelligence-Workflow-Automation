# Legal Document Intelligence & Workflow Automation
### RAG-based legal document Q&A, matter-intake workflow automation, and legal tech platform reference

## What's here

| Component | Description |
|---|---|
| `rag_pipeline/` | Document retrieval + LLM Q&A over a legal document corpus (contracts, engagement letters, case memos) |
| `workflow_automation/` | Low-code-style matter intake and conflict-check workflow, modelled as a Power Automate flow |
| `docs/legal_tech_glossary.md` | Legal tech platform and process reference (DMS, matter management, conflict checking) |
| `data/` | Synthetic legal document corpus and matter intake records |

## RAG pipeline

`rag_pipeline/ingest_documents.py` chunks and embeds a corpus of legal documents (contracts, engagement letters, memos). `rag_pipeline/legal_rag_qa.py` runs retrieval + generation over that index — answering questions like "what's the termination notice period in the Acme MSA" or "which engagement letters have a conflict waiver clause" by retrieving the relevant clause first, then generating a grounded answer.

Run:
```bash
python data/generate_legal_documents.py
python rag_pipeline/ingest_documents.py
python rag_pipeline/legal_rag_qa.py
```

## Workflow automation

`workflow_automation/matter_intake_flow.py` implements the logic of a Power Automate-style flow: new matter request comes in → conflict check runs against existing client/matter records → routes to the right practice group → notifies the relevant partner. `workflow_automation/flow_definition.json` is the flow definition itself, in the trigger/condition/action shape a Power Automate export actually takes — not just a description of one.

Run:
```bash
python workflow_automation/matter_intake_flow.py
```

## Repo structure

```
legal-tech-document-intelligence/
├── README.md
├── data/
│   └── generate_legal_documents.py       # Synthetic contracts, engagement letters, matter records
├── rag_pipeline/
│   ├── ingest_documents.py               # Chunk + embed the document corpus
│   └── legal_rag_qa.py                   # Retrieval + Q&A over the index
├── workflow_automation/
│   ├── matter_intake_flow.py             # Matter intake → conflict check → routing logic
│   └── flow_definition.json              # Power Automate-style flow definition
└── docs/
    └── legal_tech_glossary.md            # DMS, matter management, conflict checking, redlining
```
