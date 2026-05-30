# Chunking

## What is chunking?

Chunking is the process of splitting large documents into smaller pieces.

Example:

1000-page PDF
↓
Chunk 1
Chunk 2
Chunk 3
...

## Why is chunking required?

- Better retrieval
- Lower token cost
- Better embedding quality
- Fits within LLM context limits

## Chunk Overlap

Chunk overlap repeats some content between consecutive chunks.

Example:

Chunk 1:
React useEffect runs after render

Chunk 2:
runs after render and dependencies control re-execution

The repeated text is called overlap.

## Learning Notes

- Large documents should not be embedded as a single vector.
- One chunk produces one embedding.
- Chunk overlap helps preserve context.
- We used RecursiveCharacterTextSplitter.

## Flow

Document
↓
Chunking
↓
Chunks
↓
Embeddings

## Interview Question

Q. Why not create a single embedding for an entire PDF?

A. Retrieval becomes less precise and important context can be lost. Smaller chunks improve semantic search quality.