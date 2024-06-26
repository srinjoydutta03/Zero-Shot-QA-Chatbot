import React, { useState, useEffect } from "react";
import { FaSpinner } from "react-icons/fa";
import { AiOutlineSend } from "react-icons/ai";
import "./index.css"; // Ensure you have this CSS file for styling

const App = () => {
  const [conversation, setConversation] = useState({ conversation: [] });
  const [userMessage, setUserMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchConversation = async () => {
      const conversationId = localStorage.getItem("conversationId");
      if (conversationId) {
        const response = await fetch(
          `http://localhost:8001/conversations/${conversationId}`
        );
        const data = await response.json();
        if (!data.error) {
          setConversation(data);
        }
      }
    };

    fetchConversation();
  }, []);

  const generateConversationId = () =>
    "_" + Math.random().toString(36).slice(2, 11);

  const handleInputChange = (event) => {
    setUserMessage(event.target.value);
  };

  const handleNewSession = () => {
    localStorage.removeItem("conversationId");
    setConversation({ conversation: [] });
  };

  const handleSubmit = async () => {
    if (!userMessage.trim()) return;
    setIsLoading(true);
    let conversationId = localStorage.getItem("conversationId");
    if (!conversationId) {
      conversationId = generateConversationId();
      localStorage.setItem("conversationId", conversationId);
    }

    const newMessage = {
      role: "user",
      content: userMessage,
      timestamp: new Date().toISOString(),
    };

    const newConversation = [...conversation.conversation, newMessage];

    setConversation({ conversation: newConversation });
    setUserMessage("");

    try {
      const response = await fetch(
        `http://localhost:8001/conversations/${conversationId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ conversation: newConversation }),
        }
      );

      const data = await response.json();
      setConversation(data);
    } catch (error) {
      console.error("Error fetching response:", error);
      // Handle the error appropriately here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h1 className="chat-title">Zero-Shot-QA Chatbot</h1>
        <div className="message-list">
          {conversation.conversation.length > 0 && (
            <div className="messages">
              {conversation.conversation
                .filter((message) => message.role !== "system")
                .map((message, index) => (
                  <div
                    key={index}
                    className={`message ${
                      message.role === "user" ? "user-message" : "assistant-message"
                    }`}
                  >
                    <div className="message-content">
                      <span>{message.content}</span>
                    </div>
                    <span className="message-timestamp">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                ))}
              {isLoading && (
                <div className="loading">
                  <FaSpinner className="spinner" />
                  <span>Loading...</span>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={userMessage}
            onChange={handleInputChange}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                event.preventDefault();
                handleSubmit();
              }
            }}
            className="message-input"
            placeholder={isLoading ? "Processing..." : "Type your message here"}
          />
          <button onClick={handleSubmit} disabled={isLoading} className="send-button">
            <AiOutlineSend />
          </button>
        </div>
        <button onClick={handleNewSession} className="new-session-button">
          New Session
        </button>
      </div>
    </div>
  );
};

export default App;

