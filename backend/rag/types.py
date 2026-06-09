from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    content: str
    source: str
    chunk_index: int | None = None
    score: float | None = None
