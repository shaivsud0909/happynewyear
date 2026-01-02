import { useEffect, useRef, useState } from "react";

type Role = "user" | "assistant";

interface Message {
  role: Role;
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  // persistent thread id
  const threadId = useRef<string>(crypto.randomUUID());
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isStreaming) return;

    const userMessage: Message = { role: "user", content: input };

    setMessages((prev) => [...prev, userMessage, { role: "assistant", content: "" }]);
    setInput("");
    setIsStreaming(true);

    const response = await fetch("http://localhost:8000/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userMessage.content,
        thread_id: threadId.current,
      }),
    });

     const resp= await fetch("http://localhost:8000/threads");
     const data = await resp.json();

    if (!response.body) {
      setIsStreaming(false);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let assistantText = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      assistantText += decoder.decode(value);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: assistantText,
        };
        return updated;
      });
    }

    setIsStreaming(false);
  };

  return (
    <div className="flex h-screen flex-col bg-slate-900 text-gray-100">

      {/* Header */}
      <header className="bg-slate-950 p-4 text-center text-lg font-semibold">
        LangGraph Chat
      </header>

      {/* Chat window */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`max-w-[70%] rounded-xl px-4 py-2 ${
              msg.role === "user"
                ? "ml-auto bg-blue-600"
                : "mr-auto bg-slate-800"
            }`}
          >
            {msg.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="flex gap-2 bg-slate-950 p-3">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={isStreaming}
          className="flex-1 rounded-md bg-slate-800 px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="button"
          onClick={sendMessage}
          disabled={isStreaming}
          className="rounded-md bg-blue-600 px-4 py-2 font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>

    </div>
  );
}

export default App;
