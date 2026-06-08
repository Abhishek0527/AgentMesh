from rag.bm25_retriever import bm25_retrieve
from rag.retreiver import retrieve_document

def hybrid_retrieve(query,source):

    vector_results = retrieve_document(query,source)

    bm25_results = bm25_retrieve(query,source)

    if vector_results is None:
        vector_results = []

    merged = []

    for doc in vector_results:
        if doc not in merged:
            merged.append(doc)

    for doc in bm25_results:
        if doc not in merged:
            merged.append(doc)

    return merged