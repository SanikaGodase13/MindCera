from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.emotion_log import EmotionLog
from app.models.chat_conversation import ChatConversation
from app.models.chat_message import ChatMessage
from app.models.alert import Alert

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------
    # Emotion Logs
    # -----------------------
    logs = (
        db.query(EmotionLog)
        .filter(EmotionLog.user_id == current_user.id)
        .all()
    )

    # -----------------------
    # Chat Stats
    # -----------------------
    conversations = (
        db.query(ChatConversation)
        .filter(ChatConversation.user_id == current_user.id)
        .all()
    )

    messages = (
        db.query(ChatMessage)
        .join(ChatConversation)
        .filter(ChatConversation.user_id == current_user.id)
        .all()
    )

    # -----------------------
    # Alerts
    # -----------------------
    alerts = (
        db.query(Alert)
        .filter(Alert.user_id == current_user.id)
        .all()
    )

    active_alerts = sum(
        1 for a in alerts
        if a.status == "ACTIVE"
    )

    high_risk_alerts = sum(
        1 for a in alerts
        if a.risk_level == "HIGH"
    )

    # -----------------------
    # Emotion Stats
    # -----------------------
    emotions = [log.dominant_emotion for log in logs]

    emotion_counts = {}
    for e in emotions:
        emotion_counts[e] = emotion_counts.get(e, 0) + 1

    dominant_emotion = max(
        emotion_counts,
        key=emotion_counts.get
    ) if emotion_counts else None

    # -----------------------
    # Risk Stats
    # -----------------------
    risk_counts = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for log in logs:
        if log.risk_level in risk_counts:
            risk_counts[log.risk_level] += 1

    # -----------------------
    # Wellness Score (simple average logic)
    # -----------------------
    score_map = {
        "LOW": 100,
        "MEDIUM": 60,
        "HIGH": 20
    }

    scores = [
        score_map.get(log.risk_level, 50)
        for log in logs
    ]

    wellness_score = (
        sum(scores) / len(scores)
        if scores else 0
    )

    # -----------------------
    # Final Response
    # -----------------------
    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        },

        "overview": {
            "total_emotion_logs": len(logs),
            "total_conversations": len(conversations),
            "total_messages": len(messages),
            "total_alerts": len(alerts)
        },

        "wellness": {
            "wellness_score": round(wellness_score, 2),
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotion_counts,
            "risk_distribution": risk_counts
        },

        "alerts": {
            "active_alerts": active_alerts,
            "high_risk_alerts": high_risk_alerts
        }
    }