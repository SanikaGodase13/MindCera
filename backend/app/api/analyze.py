from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.sentiment_service import SentimentService
from app.services.emotion_service import EmotionService

from app.core.risk_engine import RiskEngine
from app.core.recommendation_engine import RecommendationEngine

from app.database.db import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.emotion_log import EmotionLog


router = APIRouter(prefix="/analyze", tags=["Analysis"])

sentiment_service = SentimentService()
emotion_service = EmotionService()

risk_engine = RiskEngine()
recommendation_engine = RecommendationEngine()


@router.post("/")
def analyze_text(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    text = data.get("message")

    if not text:
        return {"error": "Message is required"}

    sentiment_result = sentiment_service.predict(text)
    emotion_result = emotion_service.predict(text)

    risk_level = risk_engine.assess_risk(
        sentiment_result["sentiment"],
        emotion_result["dominant_emotion"]
    )

    recommendations = recommendation_engine.get_recommendations(
        risk_level,
        emotion_result["dominant_emotion"]
    )

    emotion_score = emotion_result["scores"][emotion_result["dominant_emotion"]]

    log = EmotionLog(
        user_id=current_user.id,
        message=text,
        sentiment=sentiment_result["sentiment"],
        sentiment_confidence=sentiment_result.get("confidence"),
        dominant_emotion=emotion_result["dominant_emotion"],
        emotion_score=emotion_score,
        risk_level=risk_level,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "sentiment": sentiment_result,
        "emotion": emotion_result,
        "risk_level": risk_level,
        "recommendations": recommendations,
    }