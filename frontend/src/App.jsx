import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";


const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState(true);

  const messagesEndRef = useRef(null);

  useEffect(() => {
   messagesEndRef.current?.scrollIntoView({
     behavior: "smooth",
   });
  }, [messages, loading]);

  useEffect(() => {

  async function checkBackend() {

    try {

      const response = await fetch(
        `${API_URL}/health`
      );

      if (!response.ok) {
        throw new Error("Backend unavailable");
      }

      setBackendOnline(true);

    } catch {

      setBackendOnline(false);

    }

  }


  checkBackend();


  const interval = setInterval(
    checkBackend,
    10000
  );


  return () => {
    clearInterval(interval);
  };

}, []);


  async function askQuestion() {

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }


    // Add user message immediately

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
      timestamp: new Date(),
    };


    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);


    setQuestion("");
    setLoading(true);


    try {

      const response = await fetch(
        `${API_URL}/ask`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: trimmedQuestion,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          data.message ||
          "Something went wrong."
        );

      }

      setBackendOnline(true);


      // Add AI response

      const assistantMessage = {
        role: "assistant",
        content: data.answer,
        timestamp: new Date(),
      };


      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);

    }

    catch (error) {

  console.error(
    "API request failed:",
    error
  );


  setBackendOnline(false);


  setMessages((previousMessages) => [
    ...previousMessages,

    {
      role: "assistant",
      content:
        "I couldn't connect to the Supply Chain AI backend. Please make sure the FastAPI server is running on port 8000.",
    },
  ]);

}

    finally {

      setLoading(false);

    }

  }


  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askQuestion();

    }

  }


  return (

    <div className="app">


      {/* HEADER */}

      <header className="header">

  <div>

    <h1>
      Supply Chain AI
    </h1>

    <p>
      Intelligent Supply Chain Assistant
    </p>

  </div>


  <div className="header-actions">

    {messages.length > 0 && (

      <button
        type="button"
        className="clear-button"
        onClick={() => setMessages([])}
        disabled={loading}
      >
        Clear Chat
      </button>

    )}


    <div className="status">

  <span
    className={`status-dot ${
      backendOnline
        ? "online"
        : "offline"
    }`}
  ></span>

  {loading
    ? "Thinking..."
    : backendOnline
      ? "Online"
      : "Offline"}

</div>

  </div>

</header>


      {/* CHAT */}

      <main className="chat-container">


        {messages.length === 0 ? (

          <div className="welcome">

  <div className="welcome-icon">
    🚚
  </div>


  <h2>
    Welcome to Supply Chain AI
  </h2>


  <p>
    Ask questions about inventory,
    suppliers, orders, products and
    your supply chain.
  </p>
  <div className="capabilities">

  <div className="capability-card">

    <div className="capability-icon">
      📦
    </div>

    <div>
      <h3>Inventory</h3>
      <p>Stock and replenishment</p>
    </div>

  </div>


  <div className="capability-card">

    <div className="capability-icon">
      🏭
    </div>

    <div>
      <h3>Suppliers</h3>
      <p>Reliability and delays</p>
    </div>

  </div>


  <div className="capability-card">

    <div className="capability-icon">
      📋
    </div>

    <div>
      <h3>Orders</h3>
      <p>Orders and status</p>
    </div>

  </div>


  <div className="capability-card">

    <div className="capability-icon">
      📊
    </div>

    <div>
      <h3>Analytics</h3>
      <p>Supply chain insights</p>
    </div>

  </div>

</div>

  <div className="suggestions">

    <button
      type="button"
      onClick={() =>
        setQuestion(
          "What is the current stock of P0084729?"
        )
      }
    >
      Current stock of P0084729
    </button>


    <button
      type="button"
      onClick={() =>
        setQuestion(
          "Which suppliers are the most dependable?"
        )
      }
    >
      Most dependable suppliers
    </button>


    <button
      type="button"
      onClick={() =>
        setQuestion(
          "Do we have any pending orders?"
        )
      }
    >
      Pending orders
    </button>


    <button
      type="button"
      onClick={() =>
        setQuestion(
          "What is the total value of all orders?"
        )
      }
    >
      Total order value
    </button>

  </div>

</div>

        ) : (

          <div className="messages">

            {messages.map(
              (message, index) => (

                <div
                  key={index}
                  className={`message ${message.role}`}
                >

                  <div className="message-label">

  {message.role === "user"
    ? "You"
    : "Supply Chain AI"}

</div>


<div className="message-content">

  {message.role === "assistant" ? (
    <ReactMarkdown>
      {message.content}
    </ReactMarkdown>
  ) : (
    message.content
  )}

</div>


{message.timestamp && (

  <div className="message-time">

    {message.timestamp.toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    })}

  </div>

)}

                </div>

              )
            )}


            {loading && (

              <div className="message assistant">

                <div className="message-label">
                  Supply Chain AI
                </div>

                <div className="message-content thinking">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

            </div>

          )}
            <div ref={messagesEndRef} />
          </div>

        )}

      </main>


      {/* INPUT */}

      <div className="input-area">

        <div className="input-wrapper">

          <input
            type="text"
            placeholder="Ask anything about your supply chain..."
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
          />


          <button
            type="button"
            onClick={askQuestion}
            disabled={
              loading ||
              !question.trim()
            }
          >

            {loading ? "..." : "➤"}

          </button>

        </div>

      </div>


    </div>

  );

}


export default App;