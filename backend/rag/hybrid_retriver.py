from rag.bm25_retriever import bm25_retrieve
from rag.retreiver import retrieve_document

def hybrid_retrieve(query):

    vector_results = retrieve_document(query)

    bm25_results = bm25_retrieve(query)

    if vector_results is None:
        vector_results = []

    merged = []
    seen = set()

    for doc in vector_results:
        key = (doc.source, doc.chunk_index, doc.content)
        if key not in seen:
            seen.add(key)
            merged.append(doc)

    for doc in bm25_results:
        key = (doc.source, doc.chunk_index, doc.content)
        if key not in seen:
            seen.add(key)
            merged.append(doc)

    return merged
