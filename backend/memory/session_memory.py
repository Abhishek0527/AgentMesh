from collections import deque
from dataclasses import dataclass
from threading import Lock


MAX_EXCHANGES = 5


@dataclass(frozen=True)
class ConversationTurn:
    query: str
    answer: str


class SessionMemory:
    def __init__(self, max_exchanges: int = MAX_EXCHANGES):
        self._turns = deque(maxlen=max_exchanges)

    def get_history_text(self) -> str:
        history_lines = []

        for turn in self._turns:
            history_lines.append(f"Human: {turn.query}")
            history_lines.append(f"AI: {turn.answer}")

        return "\n".join(history_lines)

    def append_turn(self, query: str, answer: str) -> None:
        self._turns.append(
            ConversationTurn(
                query=query,
                answer=answer,
            )
        )


_memory_store: dict[str, SessionMemory] = {}
_memory_lock = Lock()


def get_session_memory(session_id: str) -> SessionMemory:
    with _memory_lock:
        if session_id not in _memory_store:
            _memory_store[session_id] = SessionMemory()

        return _memory_store[session_id]
