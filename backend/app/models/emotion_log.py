from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from app.database.base import Base


class EmotionLog(Base):
    __tablename__ = "emotion_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    message = Column(Text, nullable=False)

    sentiment = Column(String(20))

    sentiment_confidence = Column(Float)

    dominant_emotion = Column(String(50))

    emotion_score = Column(Float)

    risk_level = Column(String(20))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )