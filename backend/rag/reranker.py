from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_documents(query: str, documents: list[str]):

    pairs = []

    for doc in documents:
        pairs.append([query, doc])

    scores = model.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_score = ranked[0][1]

    print("Top Score:", top_score)

    top_docs = [
        doc
        for doc, score in ranked[:3]
    ]

    return top_docs, top_score