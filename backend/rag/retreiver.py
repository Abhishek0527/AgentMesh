from rag.embedding import embed_query
from rag.types import RetrievedChunk
import chromadb

def  retrieve_document(query:str):
    client = chromadb.PersistentClient(path="./chroma_db")

    collection = client.get_or_create_collection(name="pdf_collection")

    query_embedding = embed_query(query)

    retrieved = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        include=["documents", "metadatas"]
    )

    documents = retrieved["documents"][0]
    metadatas = retrieved["metadatas"][0]

    print("Retrieved Chunks:", len(documents))

    return [
        RetrievedChunk(
            content=document,
            source=metadata.get("source", "Unknown"),
            chunk_index=metadata.get("chunk_index"),
        )
        for document, metadata in zip(documents, metadatas)
    ]

    # print(retrieved["metadatas"])

    # print("Query:", query)
    # # print("Distance:", retrieved["distances"][0][0])

    # best_decison = retrieved["distances"][0][0]

    # Threeshold = 1.5

    # if best_decison > Threeshold:
    #     return None
    # else:
    #     return retrieved["documents"][0]

    # return retrieved['distances']
    # return retrieved["documents"][0]

# Testing retrieve_document
# retrieved_documents = retrieve_document("What is React?")
# print(retrieved_documents)
