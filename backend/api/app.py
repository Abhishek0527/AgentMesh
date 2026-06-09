from collections.abc import Iterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

from memory.session_memory import get_session_memory
from rag.citations import build_citations
from rag.generator import generate_reponse
from rag.generator import stream_reponse
from rag.hybrid_retriver import hybrid_retrieve
from rag.reranker import rerank_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query:str
    session_id:str


def prepare_chat_context(query: str):
    retrieved_docs = hybrid_retrieve(query)

    reranked_docs, top_score = rerank_documents(
        query,
        retrieved_docs
    )

    if top_score < 0:
        print("General LLM Mode")
        return None, []

    print("RAG Mode")
    return reranked_docs, build_citations(reranked_docs)

@app.post("/chat")
def chat(req:ChatRequest):
    print("Request received:", req.query)
    query = req.query
    memory = get_session_memory(req.session_id)
    history = memory.get_history_text()

    context_documents, citations = prepare_chat_context(query)

    answer = generate_reponse(
        query,
        context_documents,
        history=history
    )

    memory.append_turn(query, answer)

    return {
        "response": answer,
        "citations": citations,
    }


@app.post("/chat/stream", response_class=EventSourceResponse)
def stream_chat(req: ChatRequest) -> Iterable[ServerSentEvent]:
    print("Streaming request received:", req.query)
    query = req.query
    memory = get_session_memory(req.session_id)
    history = memory.get_history_text()
    context_documents, citations = prepare_chat_context(query)

    def event_stream():
        answer_parts = []

        try:
            for token in stream_reponse(
                query,
                context_documents,
                history=history
            ):
                answer_parts.append(token)
                yield ServerSentEvent(
                    event="token",
                    data={
                        "text": token
                    }
                )

            answer = "".join(answer_parts)

            memory.append_turn(query, answer)

            yield ServerSentEvent(
                event="citations",
                data=citations
            )
            yield ServerSentEvent(
                event="done",
                data={
                    "answer": answer,
                    "citations": citations,
                }
            )
        except Exception as exc:
            yield ServerSentEvent(
                event="error",
                data={
                    "message": str(exc)
                }
            )

    return event_stream()
