from sentence_transformers import CrossEncoder

from rag.types import RetrievedChunk

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_documents(query: str, documents: list[RetrievedChunk]):
    if not documents:
        return [], float("-inf")

    pairs = []

    for doc in documents:
        pairs.append([query, doc.content])

    scores = model.predict(pairs)

    ranked = []

    for doc, score in zip(documents, scores):
        ranked.append(
            RetrievedChunk(
                content=doc.content,
                source=doc.source,
                chunk_index=doc.chunk_index,
                score=float(score),
            )
        )

    ranked.sort(
        key=lambda doc: doc.score if doc.score is not None else float("-inf"),
        reverse=True
    )

    top_score = ranked[0].score if ranked[0].score is not None else float("-inf")

    print("Top Score:", top_score)

    top_docs = ranked[:3]

    return top_docs, top_score
