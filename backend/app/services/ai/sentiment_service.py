from transformers import pipeline


sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_sentiment(text: str):

    result = sentiment_pipeline(text)[0]

    return {
        "sentiment": result["label"],
        "confidence": round(
            result["score"],
            4
        )
    }