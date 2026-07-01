class RiskEngine:

    def assess_risk(self, sentiment, emotion):
        
        sentiment = sentiment.upper()
        emotion = emotion.lower()

        # High Risk
        if sentiment == "NEGATIVE" and emotion in ["fear", "anger"]:
            return "HIGH"

        # Medium Risk
        if sentiment == "NEGATIVE" and emotion in ["sadness", "disgust"]:
            return "MEDIUM"

        # Low Risk
        return "LOW"