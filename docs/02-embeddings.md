# Embeddings

## What are embeddings?

Embeddings are numerical representations of text.

They convert text into vectors that capture semantic meaning.

Example:

"What is React?"
↓
[0.12, -0.45, 0.78, ...]

## Why are embeddings needed?

Computers cannot understand meaning from raw text.

Embeddings allow similarity comparison between pieces of text.

## Learning Notes

- Similar meanings have similar vectors.
- Embeddings are generated after chunking.
- One chunk produces one embedding.
- Embeddings are stored in a vector database.

## Flow

Chunk
↓
Embedding Model
↓
Vector

## Example

Chunk 1
↓
Embedding 1

Chunk 2
↓
Embedding 2

## Interview Question

Q. Why do we need embeddings in RAG?

A. Embeddings convert text into vectors so that semantically similar content can be retrieved using similarity search.