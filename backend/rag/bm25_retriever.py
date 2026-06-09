from rank_bm25 import BM25Okapi
from rag.types import RetrievedChunk
import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_collection"
)


def bm25_retrieve(
    query: str,
    top_k: int = 10
):

    retrieved = collection.get(
        include=["documents", "metadatas"]
    )
    filtered_docs = retrieved["documents"]
    filtered_metadatas = retrieved["metadatas"]

    if not filtered_docs:
        return []

    tokenized_docs = [
        doc.lower().split()
        for doc in filtered_docs
    ]

    bm25 = BM25Okapi(tokenized_docs)

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked = sorted(
        zip(filtered_docs, filtered_metadatas, scores),
        key=lambda x: x[2],
        reverse=True
    )

    top_chunks = [
        RetrievedChunk(
            content=document,
            source=metadata.get("source", "Unknown"),
            chunk_index=metadata.get("chunk_index"),
        )
        for document, metadata, score in ranked[:top_k]
    ]

    print("BM25 Docs:", len(filtered_docs))

    return top_chunks
