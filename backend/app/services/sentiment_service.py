from transformers import pipeline


class SentimentService:
    def __init__(self):
        print("Loading Sentiment Model...")

        self.model = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        )

        print("Sentiment Model Loaded Successfully!")

    def predict(self, text: str):
        result = self.model(text)[0]

        return {
            "sentiment": result["label"],
            "confidence": round(result["score"], 4)
        }