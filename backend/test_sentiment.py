from app.services.ai.sentiment_service import (
    analyze_sentiment
)

text = "I feel stressed because of my exams"

result = analyze_sentiment(text)

print(result)