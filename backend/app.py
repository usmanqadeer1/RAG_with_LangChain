from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from sse_starlette.sse import EventSourceResponse
from rag_chain import rag_chain
import asyncio
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from langchain.schema.messages import HumanMessage, AIMessage

app = FastAPI()

# Optional for React dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with actual domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    chat_history: list[Message]

@app.post("/chat")
async def chat_stream(request: Request, body: ChatRequest):
    async def generate():
        input_data = {
            "question": body.question,
            "chat_history": [
                AIMessage(content=m.content) if m.role == "assistant" else HumanMessage(content=m.content)
                for m in body.chat_history
            ]
        }

        for chunk in rag_chain.stream(input_data):
            if await request.is_disconnected():
                break
            yield chunk  # just raw string
            await asyncio.sleep(0.05)

    return StreamingResponse(generate(), media_type="text/plain")

# @app.get("/chat")
# async def chat(request: Request, query: str):
#     async def event_generator():
#         try:
#             for chunk in rag_chain.stream({"question": query}):
#                 if await request.is_disconnected():
#                     break
#                 yield f"{chunk}"
#                 await asyncio.sleep(0.05)
#             yield "event: end\ndata: [DONE]\n\n"
#         except Exception as e:
#             yield f"event: error\ndata: {str(e)}\n\n"
#     return EventSourceResponse(event_generator())