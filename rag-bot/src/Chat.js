import React, { useState, useRef, useEffect } from "react";

const Chat = () => {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]); // [{role: 'user'|'bot', content: ''}]
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedContent, setStreamedContent] = useState("");

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamedContent]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const newMessages = [...messages, { role: "user", content: question }];
    setMessages(newMessages);
    setQuestion("");
    setIsStreaming(true);
    setStreamedContent("");

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        chat_history: newMessages.map((m) => ({
          role: m.role === "bot" ? "assistant" : "user",
          content: m.content,
        })),
      }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let botReply = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      botReply += chunk;
      setStreamedContent(botReply);
    }

    setMessages((prev) => [...prev, { role: "bot", content: botReply }]);
    setIsStreaming(false);
    setStreamedContent("");
  };

  return (
    <div className="chat-container" style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <div className="chat-box" style={{ flex: 1, padding: "1rem", overflowY: "auto", background: "#f5f5f5" }}>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role}`}
            style={{
              marginBottom: "1rem",
              padding: "0.75rem",
              borderRadius: "8px",
              maxWidth: "80%",
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              backgroundColor: msg.role === "user" ? "#dbeafe" : "#e5e7eb",
              textAlign: msg.role === "user" ? "right" : "left",
            }}
          >
            {msg.content}
          </div>
        ))}

        {isStreaming && (
          <div
            className="message bot"
            style={{
              marginBottom: "1rem",
              padding: "0.75rem",
              borderRadius: "8px",
              maxWidth: "80%",
              alignSelf: "flex-start",
              backgroundColor: "#e5e7eb",
              fontStyle: "italic",
            }}
          >
            {streamedContent || "Thinking..."}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="chat-input" style={{ display: "flex", padding: "1rem", borderTop: "1px solid #ddd", backgroundColor: "white" }}>
        <textarea
          rows={2}
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ flex: 1, resize: "none", fontSize: "1rem", padding: "0.75rem", borderRadius: "8px", border: "1px solid #ccc" }}
        />
        <button
          onClick={handleAsk}
          disabled={isStreaming}
          style={{ marginLeft: "1rem", padding: "0.75rem 1.25rem", fontSize: "1rem", backgroundColor: "#2563eb", color: "white", border: "none", borderRadius: "8px", cursor: "pointer" }}
        >
          {isStreaming ? "Streaming..." : "Ask"}
        </button>
      </div>
    </div>
  );
};

export default Chat;
