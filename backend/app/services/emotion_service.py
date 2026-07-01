from transformers import pipeline


class EmotionService:
    def __init__(self):
        print("Loading Emotion Model...")

        self.model = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None
        )

        print("Emotion Model Loaded Successfully!")

    def predict(self, text: str):
        result = self.model(text)


        # Model returns a list containing all emotion scores
        emotions = result[0]

        scores = {
            emotion["label"]: emotion["score"]
            for emotion in emotions
        }

        dominant_emotion = max(scores, key=scores.get)

        return {
            "scores": scores,
            "dominant_emotion": dominant_emotion
        }