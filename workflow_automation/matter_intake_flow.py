"""
Matter intake workflow — the logic behind a Power Automate flow: new
matter request → conflict check → practice group routing → notification.
Implemented in Python here so the decision logic is testable; the JSON
flow definition alongside it (flow_definition.json) is what this would
actually look like exported from Power Automate.
"""
import json

with open("data/matter_intake_requests.json") as f:
    matters = json.load(f)

with open("data/legal_documents.json") as f:
    existing_documents = json.load(f)

existing_clients = {doc["client"] for doc in existing_documents}

PARTNER_BY_PRACTICE_GROUP = {
    "Corporate/M&A": "partner.corporate@algfirm.example",
    "Employment": "partner.employment@algfirm.example",
    "Litigation": "partner.litigation@algfirm.example",
    "Real Estate": "partner.realestate@algfirm.example",
    "Tax": "partner.tax@algfirm.example",
}


def run_conflict_check(matter: dict) -> dict:
    """Simplified conflict check: flags if the client already has other
    matters on file (a real conflict check is far more involved — adverse
    party checks, related-entity checks — this demonstrates the flow
    trigger logic, not a production conflicts database)."""
    is_existing_client = matter["client"] in existing_clients
    flagged = matter["potential_conflict"]

    if flagged:
        status = "CONFLICT_FLAGGED — Escalate to Conflicts Committee"
    elif is_existing_client:
        status = "CLEAR — Existing client, no new conflict"
    else:
        status = "CLEAR — New client, standard onboarding"

    return {"conflict_status": status, "is_existing_client": is_existing_client}


def route_matter(matter: dict, conflict_result: dict) -> dict:
    if "CONFLICT_FLAGGED" in conflict_result["conflict_status"]:
        return {
            "routed_to": "Conflicts Committee",
            "notification_sent_to": "conflicts.committee@algfirm.example",
            "action": "Hold matter intake pending committee review",
        }

    partner_email = PARTNER_BY_PRACTICE_GROUP.get(matter["practice_group_requested"], "unassigned@algfirm.example")
    return {
        "routed_to": matter["practice_group_requested"],
        "notification_sent_to": partner_email,
        "action": "Matter intake approved — partner notified for engagement letter drafting",
    }


def process_matter_intake(matter: dict) -> dict:
    conflict_result = run_conflict_check(matter)
    routing_result = route_matter(matter, conflict_result)
    return {
        "matter_id": matter["matter_id"],
        "client": matter["client"],
        **conflict_result,
        **routing_result,
    }


if __name__ == "__main__":
    results = [process_matter_intake(m) for m in matters]

    for r in results:
        print(f"{r['matter_id']} | {r['client']:25s} | {r['conflict_status']:55s} | -> {r['routed_to']}")

    conflict_count = sum(1 for r in results if "CONFLICT_FLAGGED" in r["conflict_status"])
    print(f"\nProcessed {len(results)} matter intake requests, {conflict_count} flagged for conflict review")

    with open("workflow_automation/matter_intake_results.json", "w") as f:
        json.dump(results, f, indent=2)
