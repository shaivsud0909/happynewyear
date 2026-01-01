from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from .schema import ChatRequest
from .services import get_all_threads, invoke_chat, stream_chat

router = APIRouter()

@router.get("/threads")
def threads():
    return get_all_threads()

@router.post("/chat")
def chat(req: ChatRequest):
    return invoke_chat(req.message, req.thread_id)

@router.post("/stream")
def stream(req: ChatRequest):
    return StreamingResponse(
        stream_chat(req.message, req.thread_id),
        media_type="text/plain"
    )
