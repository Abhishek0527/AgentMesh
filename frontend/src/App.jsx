import { useState } from "react";
import "./App.css";

const SESSION_STORAGE_KEY = "agentmesh-session-id";

function getSessionId() {
  const existingSessionId = window.localStorage.getItem(
    SESSION_STORAGE_KEY
  );

  if (existingSessionId) {
    return existingSessionId;
  }

  const newSessionId = window.crypto.randomUUID();

  window.localStorage.setItem(
    SESSION_STORAGE_KEY,
    newSessionId
  );

  return newSessionId;
}

function parseSseEvent(block) {
  const lines = block.split(/\r?\n/);
  let eventName = "message";
  const dataLines = [];

  for (const line of lines) {
    if (!line || line.startsWith(":")) {
      continue;
    }

    if (line.startsWith("event:")) {
      eventName = line.slice(6).trim();
      continue;
    }

    if (line.startsWith("data:")) {
      dataLines.push(line.slice(5).trimStart());
    }
  }

  if (!dataLines.length) {
    return null;
  }

  return {
    event: eventName,
    data: JSON.parse(dataLines.join("\n")),
  };
}

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!query.trim() || isStreaming) {
      return;
    }

    setAnswer("");
    setCitations([]);
    setError("");
    setIsStreaming(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({
            query: query,
            session_id: getSessionId(),
          }),
        }
      );

      if (!response.ok || !response.body) {
        setError("The server could not start the response stream.");
        setIsStreaming(false);
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const events = buffer.split(/\r?\n\r?\n/);
        buffer = events.pop() ?? "";

        for (const rawEvent of events) {
          const parsedEvent = parseSseEvent(rawEvent);

          if (!parsedEvent) {
            continue;
          }

          if (parsedEvent.event === "token") {
            setAnswer((currentAnswer) => (
              currentAnswer + parsedEvent.data.text
            ));
          }

          if (parsedEvent.event === "citations") {
            setCitations(parsedEvent.data);
          }

          if (parsedEvent.event === "error") {
            setError(parsedEvent.data.message);
            setIsStreaming(false);
            return;
          }

          if (parsedEvent.event === "done") {
            setIsStreaming(false);
          }
        }
      }

      if (buffer.trim()) {
        const parsedEvent = parseSseEvent(buffer);

        if (parsedEvent?.event === "citations") {
          setCitations(parsedEvent.data);
        }

        if (parsedEvent?.event === "done") {
          setIsStreaming(false);
        }
      }
    } catch (streamError) {
      setError(streamError.message);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <p className="eyebrow">AgentMesh</p>
        <h1 style={{ fontSize: "30px" }}>Streaming RAG with citations</h1>
        <p className="hero-copy">
          Ask a question and watch the answer stream in real time.
          When retrieval is used, the supporting chunks appear below the answer.
        </p>
      </section>

      <section className="chat-panel">
        <div className="composer">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about the indexed knowledge base"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askQuestion();
              }
            }}
          />

          <button onClick={askQuestion} disabled={isStreaming}>
            {isStreaming ? "Streaming..." : "Ask"}
          </button>
        </div>

        <section className="answer-card">
          <div className="answer-header">
            <h2>Answer</h2>
            {isStreaming ? <span className="status-pill">Live</span> : null}
          </div>

          <p className="answer-text">
            {answer || "The response will appear here as tokens arrive."}
          </p>

          {error ? (
            <p className="error-text">{error}</p>
          ) : null}
        </section>

        <section className="citations-card">
          <div className="answer-header">
            <h2>Source citations</h2>
          </div>

          {citations.length ? (
            <ul className="citation-list">
              {citations.map((citation) => (
                <li
                  key={`${citation.source}-${citation.chunk_index}`}
                  className="citation-item"
                >
                  <p className="citation-source">
                    {citation.source}
                    {citation.chunk_index !== null
                      ? ` | chunk ${citation.chunk_index}`
                      : ""}
                  </p>
                  <p className="citation-snippet">
                    {citation.snippet}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="empty-state">
              Citations will appear here when the answer uses retrieved chunks.
            </p>
          )}
        </section>
      </section>
    </main>
  );
}

export default App;
