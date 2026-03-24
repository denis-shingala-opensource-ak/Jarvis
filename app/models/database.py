"""MySQL database for conversation persistence."""
from fastapi import Depends
from sqlalchemy import VARCHAR, Enum, Null, create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime, timezone
from typing import Annotated, Optional
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

from app.core.config import settings

if not database_exists(settings.DATABASE_URL):
    create_database(settings.DATABASE_URL)

engine = create_engine(settings.DATABASE_URL)

local_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = local_session()

Base = declarative_base()

def __get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(__get_db)]

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(VARCHAR(50), nullable=False)
    middle_name = Column(VARCHAR(30))
    last_name = Column(VARCHAR(30), nullable=False)
    email = Column(VARCHAR(50), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_deleted = Column(Integer, default=0)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    is_voice = Column(Boolean, default=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="messages")

# Create all tables automatically
Base.metadata.create_all(engine)

def ensure_conversation(conversation_id: str, title: Optional[str] = None, user_id: Optional[int] = None):
    """Create a conversation if it doesn't exist."""
    try:
        row = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not row:
            now = datetime.now(timezone.utc)
            conversation = Conversation(
                id=conversation_id,
                title=title or "New Conversation",
                created_at=now,
                updated_at=now,
                user_id=user_id
            )
            db.add(conversation)
            db.commit()
    finally:
        db.close()


def save_message(
    conversation_id: str, role: str, content: str, is_voice: bool = False, user_id: Optional[int] = None
):
    """Persist a single message."""
    ensure_conversation(conversation_id, user_id=user_id)
    now = datetime.now(timezone.utc).isoformat()

    try:
        new_message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            is_voice=int(is_voice),
            timestamp=now
        )

        db.add(new_message)
        db.commit()
    finally:
        db.close()

def get_conversations(
    user_id: int
) -> dict[str, list[dict]]:
    """Retrieve all conversations as {conversation_id: [messages]}."""
    rows = db.query(Conversation).filter(Conversation.user_id == user_id, Conversation.is_deleted == 0).all()
    result = {}
    for row in rows:
        messages = db.query(Message).filter(Message.conversation_id == row.id).order_by(Message.id).all()
        result[row.id] = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    return result

def get_conversation_history(
    conversation_id: str, limit: int = 50
) -> list[dict]:
    """Retrieve recent messages for a conversation."""
    rows = db.query(Message).filter(Message.conversation_id == conversation_id).limit(limit).all()
    return [
        {
            "role": row.role,
            "content": row.content,
            "is_voice": bool(row.is_voice),
            "timestamp": row.timestamp,
        }
        for row in rows
    ]


def list_conversations() -> list[dict]:
    """List all conversations with message counts."""
    rows = db.query(Conversation).filter(Conversation.is_deleted == 0).group_by(Conversation.id).order_by(Conversation.updated_at.desc()).all()
    result = []
    for row in rows:
        message_count = db.query(Message).filter(Message.conversation_id == row.id).count()
        result.append({
            "conversation_id": row.id,
            "title": row.title,
            "message_count": message_count,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        })
    return result


def delete_conversation(conversation_id: str) -> bool:
    """Soft-delete a conversation."""
    try:
        row = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not row:
            return False
        row.is_deleted = 1
        db.commit()
        return True
    finally:
        db.close()