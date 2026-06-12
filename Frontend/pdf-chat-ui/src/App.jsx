import { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Upload PDF
  const uploadPDF = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await axios.post("http://localhost:8000/upload", formData);

      alert(res.data.message || "Uploaded successfully");
    } catch (err) {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  // Ask question
  const askQuestion = async () => {
    if (!question.trim()) return;

    const userMsg = { role: "user", text: question };

    setMessages((prev) => [...prev, userMsg]);

    const currentQuestion = question;
    setQuestion("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question: currentQuestion,
      });

      const botMsg = {
        role: "bot",
        text: res.data.answer,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error getting response from server" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <header className="header">
        📄 PDF Chat Assistant (RAG + Gemini)
      </header>
      <div className="upload-section">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={uploadPDF} disabled={loading}>
          Upload PDF
        </button>
      </div>

      <div className="chat-box">
        {messages.length === 0 && (
          <div className="empty-state">
            Upload a PDF and start asking questions
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}

        {loading && <div className="loading">Thinking...</div>}
      </div>

      <div className="input-box">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about your PDF..."
        />

        <button onClick={askQuestion}>Send</button>
      </div>
    </div>
  );
}