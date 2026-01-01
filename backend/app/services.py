from langchain_core.messages import HumanMessage
from .graph import chatbot,checkpointer
import uuid


def get_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)


def invoke_chat(message: str, thread_id: str | None):
    thread_id = thread_id or str(uuid.uuid4())

    result = chatbot.invoke(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"thread_id": thread_id}}
    )

    return {
        "thread_id": thread_id,
        "response": result["messages"][-1].content
    }


def stream_chat(message: str, thread_id: str | None):
    thread_id = thread_id or str(uuid.uuid4())

    for chunk, _ in chatbot.stream(
        {"messages": [HumanMessage(content=message)]},
        config={"configurable": {"thread_id": thread_id}},
        stream_mode="messages"
    ):
        if hasattr(chunk, "content"):
            if isinstance(chunk.content, str):
                yield chunk.content
            elif isinstance(chunk.content, list):
                for part in chunk.content:
                    yield part.get("text", "")
