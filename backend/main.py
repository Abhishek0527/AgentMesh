from rag.document_loader import load_pdf
from rag.chunker import chunk_text

def main():
    pdf_path = r"C:\Users\Owner\Downloads\reactpdf.pdf"

    text = load_pdf(pdf_path)

    chunks = chunk_text(text)
    print(f"Total Chunks: {len(chunks)}")
    print("\nFirst Chunk:\n")
    print(chunks[0])


if __name__ == "__main__":
    main()
