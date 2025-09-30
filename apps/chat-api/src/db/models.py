from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Index , Float
from sqlalchemy.sql import func
from .session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', full_name='{self.full_name}')>"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    # Identificador de sesión que usa el frontend para agrupar mensajes
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, nullable=False)  # user | assistant | system
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index("ix_messages_conversation_created", "conversation_id", "created_at"),
    )

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment_pos = Column(Float, nullable=False)
    sentiment_neg = Column(Float, nullable=False)
    sentiment_neu = Column(Float, nullable=False)
    sentiment_compound = Column(Float, nullable=False)
    polarity = Column(Float, nullable=False)
    subjectivity = Column(Float, nullable=False)    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    llm_explanation = Column(String, nullable=False, default="No explanation available")
    user_id = Column(Integer, nullable=True)

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    
    # Referencia al análisis que causó este feedback
    triggered_by_analysis_id = Column(Integer, ForeignKey("analyses.id"))
    
    # Análisis del feedback mismo
    feedback_sentiment_compound = Column(Float)
    feedback_sentiment_analysis = Column(Text)
    
    # Admin fields
    resolved = Column(Boolean, default=False)
    admin_notes = Column(Text)
    
    created_at = Column(DateTime, default=func.now())
    
    