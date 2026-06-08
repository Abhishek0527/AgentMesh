from rag.vectorstore import store_embeddings
from rag.embedding import embed_chunks
from rag.chunker import chunk_text
from rag.document_loader import load_pdf
import os

def ingest():

    pdf_folder = "./pdf_documents"

    pdf_files = [
        file
        for file in os.listdir(pdf_folder)
        if file.endswith(".pdf")
    ]

    for pdf_file in pdf_files:

        pdf_path = os.path.join(
            pdf_folder,
            pdf_file
        )

        print(f"\nProcessing: {pdf_file}")

        text = load_pdf(pdf_path)

        chunks = chunk_text(text)

        metadatas = []

        for index, _ in enumerate(chunks):
            metadatas.append(
                {
                    "source": pdf_file,
                    "chunk_index": index
                }
            )

        embeddings = embed_chunks(chunks)

        store_embeddings(
            chunks,
            embeddings,
            metadatas
        )

        print(f"Finished: {pdf_file}")
        print(f"Chunks Stored: {len(chunks)}")


if __name__ == "__main__":
    ingest()

# def ingest():
#     pdf_path = r"C:\Users\Owner\Downloads\reactpdf.pdf"

#     source = os.path.basename(pdf_path)

#     metadatas = []



#     text = load_pdf(pdf_path)

#     chunks = chunk_text(text)

#     for _ in chunks:
#         metadatas.append(
#             {
#                 "source": source
#             }
#     )

#     # print(f"Total Chunks: {len(chunks)}")

#     embeddings = embed_chunks(chunks)

#     # print(f"Total Embeddings: {len(embeddings)}")

#     store_embeddings(chunks,embeddings,metadatas)
#  ---------------this is used for single source of pdf-----------