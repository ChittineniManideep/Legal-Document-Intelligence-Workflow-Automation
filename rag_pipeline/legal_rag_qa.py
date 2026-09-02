"""
Retrieval + answer generation over the legal document index. Retrieval
uses cosine similarity against the TF-IDF index built in ingest_documents.py.
Generation is template-based here (extractive, grounded directly in the
retrieved chunk) rather than calling an LLM API, so this runs standalone —
in the full system this generation step is where LangChain + an LLM call
would replace the template, using the same retrieved-chunk context.
"""
import pickle
from sklearn.metrics.pairwise import cosine_similarity

with open("rag_pipeline/index.pkl", "rb") as f:
    index = pickle.load(f)

chunks = index["chunks"]
vectorizer = index["vectorizer"]
matrix = index["matrix"]


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()
    top_indices = scores.argsort()[::-1][:top_k]
    return [
        {**chunks[i], "relevance_score": round(float(scores[i]), 3)}
        for i in top_indices if scores[i] > 0
    ]


def answer_question(query: str) -> dict:
    retrieved = retrieve(query, top_k=3)
    if not retrieved:
        return {"query": query, "answer": "No relevant clause found in the indexed documents.", "sources": []}

    top_chunk = retrieved[0]
    answer = f"Based on {top_chunk['doc_id']} ({top_chunk['doc_type']}, {top_chunk['client']}): {top_chunk['chunk_text']}"
    return {
        "query": query,
        "answer": answer,
        "sources": [{"doc_id": r["doc_id"], "relevance_score": r["relevance_score"]} for r in retrieved],
    }


if __name__ == "__main__":
    test_queries = [
        "What is the termination notice period in the master services agreement?",
        "Are there any conflict waivers in engagement letters?",
        "What is the recommendation on the employment dispute matter?",
        "What is the liability cap under the services agreement?",
    ]
    for q in test_queries:
        result = answer_question(q)
        print(f"\nQ: {result['query']}")
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")
