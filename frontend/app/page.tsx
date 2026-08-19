"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

type Msg = {
  role: "doctor" | "palto";
  text: string;
  sources?: any[];
  meta?: any;
};

const PALTO_NAME = "بَالطُّو'";

export default function Home() {
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "palto",
      text: `Hello. I'm ${PALTO_NAME}, an evidence-grounded clinical assistant. How can I help?`,
    },
  ]);

  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  async function send() {
    if (!input.trim() || busy) return;

    const q = input.trim();

    setInput("");

    // Add doctor's message
    setMessages((m) => [
      ...m,
      {
        role: "doctor",
        text: q,
      },
    ]);

    setBusy(true);

    try {
      const r = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: q,
          session_id: "demo-session",
        }),
      });

      if (!r.ok) {
        throw new Error("Backend request failed");
      }

      const data = await r.json();

      // Add PALTO response only once
      setMessages((m) => [
        ...m,
        {
          role: "palto",
          text: data.answer || "",
          sources: data.sources || [],
          meta: data,
        },
      ]);
    } catch (error) {
      setMessages((m) => [
        ...m,
        {
          role: "palto",
          text: `${PALTO_NAME} could not reach the backend. Make sure FastAPI is running.`,
        },
      ]);
    } finally {
      setBusy(false);
    }
  }

  function newChat() {
    setMessages([
      {
        role: "palto",
        text: `Hello. I'm ${PALTO_NAME}, an evidence-grounded clinical assistant. How can I help?`,
      },
    ]);

    setInput("");
  }

  return (
    <div className="app-shell">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="sidebar-top">

          <div className="brand">
            {PALTO_NAME}
          </div>

          <button
            className="new-chat"
            onClick={newChat}
          >
            <span className="plus">+</span>
            New Chat
          </button>

        </div>


        {/* ================= CONVERSATIONS ================= */}

        <div className="sidebar-section">

          <div className="section-title">
            Recent Conversations
          </div>


          <div className="conversation active">

            <span className="conversation-icon">
              ▢
            </span>

            <div>

              <div className="conversation-title">
                Metformin and Cephalexin
              </div>

              <div className="conversation-time">
                Just now
              </div>

            </div>

          </div>


          <div className="conversation">

            <span className="conversation-icon">
              ▢
            </span>

            <div>

              <div className="conversation-title">
                Drug interactions
              </div>

              <div className="conversation-time">
                1 hour ago
              </div>

            </div>

          </div>


          <div className="conversation">

            <span className="conversation-icon">
              ▢
            </span>

            <div>

              <div className="conversation-title">
                Hypertension review
              </div>

              <div className="conversation-time">
                Yesterday
              </div>

            </div>

          </div>


          <div className="conversation">

            <span className="conversation-icon">
              ▢
            </span>

            <div>

              <div className="conversation-title">
                Medication safety
              </div>

              <div className="conversation-time">
                2 days ago
              </div>

            </div>

          </div>

        </div>


        {/* ================= CLINICAL CARD ================= */}

        <div className="clinical-card">

          <div className="clinical-card-title">

            <span className="shield">
              ◆
            </span>

            Clinical AI Assistant

          </div>

          <p>
            {PALTO_NAME} provides evidence-grounded
            clinical information and does not
            replace professional medical judgment.
          </p>

        </div>


        {/* ================= PROFILE ================= */}

        <div className="profile">

          <div className="avatar">
            D
          </div>

          <div className="profile-info">

            <div className="profile-name">
              Doctor
            </div>

            <div className="profile-role">
              Clinical User
            </div>

          </div>

          <span className="profile-arrow">
            ˅
          </span>

        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main">


        {/* ================= HEADER ================= */}

        <header className="main-header">

          <div className="header-logo">
            {PALTO_NAME}
          </div>

          <div className="header-status">

            <span className="status-dot"></span>

            Evidence-Grounded

          </div>

        </header>


        {/* ================= CHAT ================= */}

        <section className="chat-area">

          {messages.length === 1 && !busy ? (

            <div className="welcome">

              <div className="welcome-symbol">

                <div className="symbol-star">
                  *
                </div>

                <div className="symbol-hand">
                  ≋
                </div>

                <div className="symbol-dot">
                  ◆
                </div>

              </div>


              <h1>
                {PALTO_NAME}
              </h1>

              <p>
                Your Evidence-Grounded Clinical AI Assistant
              </p>

            </div>

          ) : (

            <div className="messages">

              {messages.map((m, i) => (

                <div
                  key={i}
                  className={`message-row ${m.role}`}
                >

                  {/* ================= MESSAGE NAME ================= */}

                  <div className="message-name">

                    {m.role === "doctor"
                      ? "Doctor"
                      : PALTO_NAME}

                  </div>


                  {/* ================= MESSAGE CONTENT ================= */}

                  <div
                    className="message-content"
                    dir="auto"
                  >

                    <ReactMarkdown
                      components={{

                        h1: ({ children }) => (
                          <h1 className="md-h1">
                            {children}
                          </h1>
                        ),

                        h2: ({ children }) => (
                          <h2 className="md-h2">
                            {children}
                          </h2>
                        ),

                        h3: ({ children }) => (
                          <h3 className="md-h3">
                            {children}
                          </h3>
                        ),

                        h4: ({ children }) => (
                          <h4 className="md-h4">
                            {children}
                          </h4>
                        ),

                        p: ({ children }) => (
                          <p className="md-p">
                            {children}
                          </p>
                        ),

                        ul: ({ children }) => (
                          <ul className="md-ul">
                            {children}
                          </ul>
                        ),

                        ol: ({ children }) => (
                          <ol className="md-ol">
                            {children}
                          </ol>
                        ),

                        li: ({ children }) => (
                          <li className="md-li">
                            {children}
                          </li>
                        ),

                        strong: ({ children }) => (
                          <strong className="md-strong">
                            {children}
                          </strong>
                        ),

                        em: ({ children }) => (
                          <em className="md-em">
                            {children}
                          </em>
                        ),

                        blockquote: ({ children }) => (
                          <blockquote className="md-blockquote">
                            {children}
                          </blockquote>
                        ),

                        hr: () => (
                          <hr className="md-hr" />
                        ),

                        code: ({ children }) => (
                          <code className="md-code">
                            {children}
                          </code>
                        ),

                        pre: ({ children }) => (
                          <pre className="md-pre">
                            {children}
                          </pre>
                        ),

                        table: ({ children }) => (
                          <table className="md-table">
                            {children}
                          </table>
                        ),

                        thead: ({ children }) => (
                          <thead className="md-thead">
                            {children}
                          </thead>
                        ),

                        tbody: ({ children }) => (
                          <tbody className="md-tbody">
                            {children}
                          </tbody>
                        ),

                        tr: ({ children }) => (
                          <tr className="md-tr">
                            {children}
                          </tr>
                        ),

                        th: ({ children }) => (
                          <th className="md-th">
                            {children}
                          </th>
                        ),

                        td: ({ children }) => (
                          <td className="md-td">
                            {children}
                          </td>
                        ),

                        a: ({ children, href }) => (
                          <a
                            className="md-link"
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {children}
                          </a>
                        ),

                      }}
                    >
                      {m.text}
                    </ReactMarkdown>

                  </div>


                  {/* ================= SOURCES ================= */}

                  {m.sources &&
                    m.sources.length > 0 && (

                      <div className="sources">

                        <div className="sources-title">
                          Sources
                        </div>

                        {m.sources.map(
                          (source: any, j: number) => (

                            <div
                              className="source-item"
                              key={j}
                            >
                              {source.title ||
                                "Clinical source"}
                            </div>

                          )
                        )}

                      </div>

                    )}

                </div>

              ))}

            </div>

          )}


          {/* ================= THINKING ================= */}

          {busy && (

            <div className="thinking">

              <div className="thinking-spinner"></div>

              <span>
                {PALTO_NAME} is thinking...
              </span>

            </div>

          )}

        </section>


        {/* ================= COMPOSER ================= */}

        <div className="composer-wrapper">

          <div className="composer">

            <input
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  send();
                }

              }}
              placeholder="Ask a clinical question..."
              disabled={busy}
            />

            <button
              className="send-button"
              onClick={send}
              disabled={
                busy || !input.trim()
              }
            >
              ↑
            </button>

          </div>


          <div className="composer-note">

            {PALTO_NAME} can make mistakes.
            Verify critical clinical information
            with authoritative sources.

          </div>

        </div>

      </main>

    </div>
  );
}