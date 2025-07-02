import { useState } from "react";
import { db } from "./firebaseConfig";
import { doc, onSnapshot } from "firebase/firestore";
import axios from "axios";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setResponse("");
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("http://localhost:8000/generate", { prompt });
      const { request_id } = res.data;

      const docRef = doc(db, "ai_responses", request_id);

      const unsubscribe = onSnapshot(docRef, (snap) => {
        if (snap.exists()) {
          const data = snap.data();
          if (data.status === "completed") {
            setResponse(data.response);
            setHistory((prev) => [
              ...prev,
              { prompt, response: data.response },
            ]);
            setLoading(false);
            setPrompt("");
            unsubscribe();
          }
        }
      });
    } catch (e) {
      setLoading(false);
      setError("An error occurred while querying the AI.");
    }
  };

  return (
    <div className="app-container">
      <h2 className="app-title">AI Streaming Demo</h2>
      <div className="form-row">
        <input
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Ask something to the AI..."
          className="prompt-input"
        />
        <button
          onClick={handleSubmit}
          disabled={loading || !prompt.trim()}
          className="send-btn"
        >
          {loading ? "Processing..." : "Send"}
        </button>
      </div>
      {error && <div className="error-message">{error}</div>}
      {response && (
        <div className="response-box">
          {response}
        </div>
      )}
      <hr className="history-section" />
      <h3 className="history-title">History</h3>
      <ul className="history-list">
        {history.slice().reverse().map((item, i) => (
          <li key={i} className="history-item">
            <div className="history-prompt"><b>Question:</b> {item.prompt}</div>
            <div><b>Answer:</b> {item.response}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
