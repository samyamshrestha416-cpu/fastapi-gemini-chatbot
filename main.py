from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db import get_db, create_table
import models, services, llm

create_table()
app = FastAPI()

class ChatRequest(BaseModel):
    conversation_id: int = Field(ge=1)
    message: str = Field(min_length=1)

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    history = services.get_history(db, request.conversation_id)
    try:
        reply = llm.get_reply(history, request.message)
    except Exception:
        raise HTTPException(status_code=502, detail="The AI service failed, try again")
    services.save_message(db, request.conversation_id, "user", request.message)
    services.save_message(db, request.conversation_id, "model", reply)
    return {"reply": reply}