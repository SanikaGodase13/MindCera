from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.emotion_log import EmotionLog
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    logs = (
        db.query(EmotionLog)
        .filter(
                EmotionLog.user_id == current_user.id
        )
        .order_by(
                EmotionLog.created_at.desc()
        )
        .all()
    )

    return logs