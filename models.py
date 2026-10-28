from db import Base
from sqlalchemy import Integer ,Column ,String,Text

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer , primary_key=True , index=True)
    conversation_id =Column(Integer , index=True)
    role =Column(String ,index=True)
    content = Column(Text ,index=True)
