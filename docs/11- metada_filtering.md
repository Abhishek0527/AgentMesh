1_metadata_filtering_and_multi_pdf.md
Problem Statement

Initially the system supported only one PDF.

Enterprise systems typically contain thousands of documents.

We need a mechanism to search specific documents.

Metadata

Metadata is information stored alongside chunks.

Example:

{
    "source": "react.pdf",
    "chunk_index": 25
}
Why Store Metadata?

Metadata enables:

Document Filtering
Source Tracking
Citations
Access Control
Future Enhancements
Multi-PDF Ingestion

Instead of processing one PDF:

react.pdf

the system processes:

documents/
├── react.pdf
├── python.pdf
├── langgraph.pdf

Each PDF is:

Load
↓
Chunk
↓
Embed
↓
Store
ChromaDB Storage

All chunks are stored in a single collection.

Example:

Chunk A
Source: react.pdf

Chunk B
Source: python.pdf

Chunk C
Source: langgraph.pdf
Metadata Filtering

User selects:

react.pdf

Retriever applies:

where={
    "source": "react.pdf"
}

Only React chunks participate in retrieval.

Benefits
Faster Search

Search space is reduced.

Better Accuracy

Irrelevant documents are excluded.

Enterprise Scalability

Thousands of documents can be managed in a single collection.

Project Flow
User Query
+
Selected Document
↓
Metadata Filter
↓
Relevant Chunks
↓
Hybrid Search
↓
Re-rank
↓
LLM
Interview Questions
What is Metadata?
Why is Metadata Filtering useful?
Why store all documents in one collection?
How does Multi-PDF retrieval work?
Why filter before retrieval?
Key Takeaway

Metadata Filtering reduces search space and enables scalable multi-document retrieval systems.

Ye 4 files likh lo. Iske baad LangGraph start karenge aur wahan bhi isi level ki documentation maintain karenge. 🚀