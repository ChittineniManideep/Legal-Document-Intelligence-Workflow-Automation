"""
Synthetic legal document corpus: contracts, engagement letters, and matter
records — shaped like what a law firm's DMS actually holds, for the RAG
pipeline to index and the workflow automation to route.
"""
import json
import random

random.seed(2)

CLIENTS = ["Acme Manufacturing Ltd", "Beacon Retail Group", "Corrib Energy plc",
           "Dunmore Logistics", "Emerald Biotech", "Fenway Capital Partners"]

CONTRACT_TEMPLATES = [
    {
        "doc_id": "CTR-{i}",
        "doc_type": "Master Services Agreement",
        "client": None,
        "text": (
            "This Master Services Agreement is entered into between {client} and the Firm. "
            "Termination: Either party may terminate this Agreement upon 90 days' written notice. "
            "Governing Law: This Agreement is governed by the laws of Ireland. "
            "Confidentiality: Both parties agree to maintain confidentiality of all shared information "
            "for a period of 5 years following termination. Limitation of Liability: Liability under "
            "this Agreement is capped at the fees paid in the preceding 12 months."
        ),
    },
    {
        "doc_id": "ENG-{i}",
        "doc_type": "Engagement Letter",
        "client": None,
        "text": (
            "Engagement Letter for {client} regarding advisory services on a proposed corporate "
            "restructuring. Scope: Advice on share transfer mechanics and tax implications. "
            "Conflict Waiver: Client acknowledges the Firm also acts for a counterparty in an unrelated "
            "matter and consents to continued representation subject to information barriers. "
            "Fees: Billed on a time-and-materials basis, invoiced monthly."
        ),
    },
    {
        "doc_id": "MEMO-{i}",
        "doc_type": "Case Memo",
        "client": None,
        "text": (
            "Internal memo regarding {client}'s employment dispute matter. Summary: Former employee "
            "alleges unfair dismissal under the Unfair Dismissals Acts 1977-2015. Recommendation: "
            "Proceed to WRC mediation before considering a full hearing, given the cost/time trade-off. "
            "Risk assessment: Medium — documentation gaps in the performance review file."
        ),
    },
]

documents = []
for i in range(1, 21):
    template = random.choice(CONTRACT_TEMPLATES)
    client = random.choice(CLIENTS)
    documents.append({
        "doc_id": template["doc_id"].format(i=i),
        "doc_type": template["doc_type"],
        "client": client,
        "text": template["text"].format(client=client),
    })

with open("data/legal_documents.json", "w") as f:
    json.dump(documents, f, indent=2)

# Matter intake records for the workflow automation piece
practice_groups = ["Corporate/M&A", "Employment", "Litigation", "Real Estate", "Tax"]
matters = []
for i in range(1, 16):
    matters.append({
        "matter_id": f"MAT-{1000+i}",
        "client": random.choice(CLIENTS),
        "practice_group_requested": random.choice(practice_groups),
        "description": "New matter intake request",
        "potential_conflict": random.random() < 0.2,  # ~20% flag a conflict for the demo
    })

with open("data/matter_intake_requests.json", "w") as f:
    json.dump(matters, f, indent=2)

print(f"Documents: {len(documents)}, Matter intake requests: {len(matters)}")
