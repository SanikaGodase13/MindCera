from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func
from app.database.base import Base


class MonitoredFolder(Base):
    __tablename__ = "monitored_folders"

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

    folder_name = Column(
        String,
        nullable=False
    )

    folder_path = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_scanned_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    last_file_count = Column(
        Integer,
        default=0
    )