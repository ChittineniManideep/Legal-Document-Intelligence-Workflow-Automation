# Legal Tech Platform & Process Reference

| Term | Definition | Where it shows up |
|---|---|---|
| **DMS (Document Management System)** | The core system a law firm stores, versions, and secures documents in — iManage and NetDocuments are the two dominant platforms in this space | `data/legal_documents.json` shaped like a DMS document export |
| **iManage** | The most widely used legal DMS, also offering workflow and email management (iManage Work) | Referenced here as the platform this project's document model is shaped after |
| **NetDocuments** | Cloud-native DMS alternative to iManage, common at mid-size and cloud-first firms | — |
| **HighQ** | A client collaboration and workflow platform (Thomson Reuters) used for client portals, deal rooms, and matter workflow | Conceptually analogous to the matter intake flow built here |
| **Contract Express** | A document automation platform (Thomson Reuters) for generating contracts from templates and questionnaires | — |
| **Matter** | The core unit of work in a law firm — a specific client engagement, distinct from the "case" terminology used in litigation-only contexts | `matter_id` throughout |
| **Conflict check** | The mandatory process of checking a new matter/client against existing client and adverse-party records before a firm can accept the engagement — a professional obligation, not just good practice | `workflow_automation/matter_intake_flow.py` |
| **Engagement letter** | The formal document defining the scope, fees, and terms of a client engagement — the legal equivalent of a statement of work | `data/legal_documents.json` |
| **Practice group** | The internal specialization a matter is routed to (Corporate/M&A, Employment, Litigation, Real Estate, Tax, etc.) | `PARTNER_BY_PRACTICE_GROUP` |
| **Redlining** | The process of marking up contract drafts with tracked changes during negotiation — a major use case for legal AI tools (redline summarization, clause comparison) | Not directly modelled here — flagged as a natural extension of the RAG pipeline |
| **WRC (Workplace Relations Commission)** | The Irish statutory body handling employment disputes, referenced in the employment case memo | `data/legal_documents.json` |
