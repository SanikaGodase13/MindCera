from transformers import pipeline

# load model directly (no service file needed)
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

text = "I feel scared and unsafe walking alone at night"

result = emotion_model(text)[0]

# format output
emotion_scores = {r["label"]: r["score"] for r in result}

dominant_emotion = max(emotion_scores, key=emotion_scores.get)

print("\nEmotion Scores:")
for k, v in emotion_scores.items():
    print(f"{k}: {v:.4f}")

print("\nDominant Emotion:", dominant_emotion)