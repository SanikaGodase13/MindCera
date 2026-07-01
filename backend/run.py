from app.services.sentiment_service import SentimentService
from app.services.emotion_service import EmotionService

from app.core.risk_engine import RiskEngine
from app.core.recommendation_engine import RecommendationEngine


sentiment_service = SentimentService()
emotion_service = EmotionService()

risk_engine = RiskEngine()
recommendation_engine = RecommendationEngine()


text = "I feel scared and unsafe walking alone at night"


sentiment_result = sentiment_service.predict(text)
emotion_result = emotion_service.predict(text)

risk = risk_engine.assess_risk(
    sentiment_result["sentiment"],
    emotion_result["dominant_emotion"]
)

recommendation = recommendation_engine.get_recommendations(
    risk,
    emotion_result["dominant_emotion"]
)

print("\nSentiment Result:")
print(sentiment_result)

print("\nEmotion Result:")
print(emotion_result)

print("\nRisk Level:")
print(risk)

print("\nRecommendations:")
print(recommendation)