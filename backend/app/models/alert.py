from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.database.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    conversation_id = Column(
        Integer,
        ForeignKey("chat_conversations.id"),
        nullable=True
    )

    risk_level = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    status = Column(
        String,
        default="ACTIVE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )