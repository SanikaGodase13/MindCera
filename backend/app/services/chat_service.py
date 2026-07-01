from app.services.sentiment_service import SentimentService
from app.services.emotion_service import EmotionService

from app.core.risk_engine import RiskEngine


class ChatService:

    def __init__(self):

        self.sentiment_service = SentimentService()

        self.emotion_service = EmotionService()

        self.risk_engine = RiskEngine()

    def analyze_message(
        self,
        message: str
    ):

        sentiment = (
            self.sentiment_service.predict(message)
        )

        emotion = (
            self.emotion_service.predict(message)
        )

        risk = (
            self.risk_engine.assess_risk(
                sentiment["sentiment"],
                emotion["dominant_emotion"]
            )
        )

        return {
            "sentiment": sentiment,
            "emotion": emotion,
            "risk": risk
        }