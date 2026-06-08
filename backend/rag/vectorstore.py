import chromadb
import uuid


def store_embeddings(chunks:list[str],embeddings:list[list[float]],metadatas:list[dict]):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="pdf_collection")

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    # for i in range(len(chunks)):
    #     ids.append(str(i))

    collection.add(
        embeddings = embeddings,
        documents=chunks,
        ids = ids,
        metadatas =metadatas
    )

    # return collection
    print(f"Stored {collection.count()} records")
