from models import Chat
from sqlalchemy.orm import Session


def save_message(db: Session, conversation_id: int, role: str, content: str):
    message = Chat(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_history(db: Session, conversation_id: int):
    rows = (
        db.query(Chat)
        .filter(Chat.conversation_id == conversation_id)
        .order_by(Chat.id)
        .all()
    )
    history = []
    for row in rows:
        history.append({"role": row.role, "content": row.content})
    return history

# if __name__ == "__main__":
#     from db import Sessionlocal
#     db = Sessionlocal()
#     save_message(db, 1, "user", "Hello")
#     save_message(db, 1, "model", "Hi there!")
#     print(get_history(db, 1))
#     db.close()