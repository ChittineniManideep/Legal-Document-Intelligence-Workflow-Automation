"""
Chunk and embed the legal document corpus using TF-IDF vectors — a
self-contained retrieval index that runs without an external embeddings
API, so this pipeline is fully runnable/testable offline. In production
this would swap TF-IDF for OpenAI/sentence-transformer embeddings; the
retrieval and chunking logic downstream is unchanged either way.
"""
import json
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

with open("data/legal_documents.json") as f:
    documents = json.load(f)


def chunk_text(text: str, chunk_size: int = 200) -> list[str]:
    """Sentence-aware chunking — splits on sentence boundaries and groups
    into ~chunk_size-character chunks, rather than a naive character-count
    split that could cut a clause mid-sentence."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""
    for sent in sentences:
        if len(current) + len(sent) > chunk_size and current:
            chunks.append(current.strip())
            current = sent
        else:
            current += " " + sent
    if current.strip():
        chunks.append(current.strip())
    return chunks


chunk_records = []
for doc in documents:
    for i, chunk in enumerate(chunk_text(doc["text"])):
        chunk_records.append({
            "chunk_id": f"{doc['doc_id']}-c{i}",
            "doc_id": doc["doc_id"],
            "doc_type": doc["doc_type"],
            "client": doc["client"],
            "chunk_text": chunk,
        })

vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
chunk_texts = [c["chunk_text"] for c in chunk_records]
tfidf_matrix = vectorizer.fit_transform(chunk_texts)

with open("rag_pipeline/index.pkl", "wb") as f:
    pickle.dump({"chunks": chunk_records, "vectorizer": vectorizer, "matrix": tfidf_matrix}, f)

print(f"Indexed {len(chunk_records)} chunks from {len(documents)} documents")
