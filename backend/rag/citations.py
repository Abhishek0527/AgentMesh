import re

from rag.types import RetrievedChunk


def build_citations(
    documents: list[RetrievedChunk],
    snippet_length: int = 180,
) -> list[dict]:
    citations = []
    seen = set()

    for document in documents:
        key = (
            document.source,
            document.chunk_index,
            document.content,
        )

        if key in seen:
            continue

        seen.add(key)

        snippet = re.sub(
            r"\s+",
            " ",
            document.content
        ).strip()[:snippet_length]

        citations.append(
            {
                "source": document.source,
                "chunk_index": document.chunk_index,
                "snippet": snippet,
            }
        )

    return citations
