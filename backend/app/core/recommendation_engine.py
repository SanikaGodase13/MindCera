class RecommendationEngine:

    def get_recommendations(self, risk_level, emotion):

        emotion = emotion.lower()

        recommendations = {
            "risk_level": risk_level,
            "emotion": emotion,
            "message": "",
            "recommendations": []
        }

        # HIGH RISK
        if risk_level == "HIGH":

            recommendations["message"] = (
                "You appear to be experiencing intense emotional distress."
            )

            recommendations["recommendations"] = [
                "Contact a trusted friend or family member.",
                "Practice grounding techniques such as the 5-4-3-2-1 method.",
                "Move to a safe and comfortable environment.",
                "Consider reaching out to a mental health professional.",
                "Use emergency support resources if needed."
            ]

        # MEDIUM RISK
        elif risk_level == "MEDIUM":

            recommendations["message"] = (
                "You may be experiencing emotional discomfort that deserves attention."
            )

            recommendations["recommendations"] = [
                "Take a short break and focus on self-care.",
                "Practice deep breathing exercises.",
                "Write down your thoughts in a journal.",
                "Talk to someone you trust.",
                "Engage in a relaxing activity."
            ]

        # LOW RISK
        else:

            recommendations["message"] = (
                "Your emotional state appears relatively stable."
            )

            recommendations["recommendations"] = [
                "Continue maintaining healthy habits.",
                "Practice gratitude and positive reflection.",
                "Stay connected with friends and family.",
                "Maintain a healthy sleep schedule.",
                "Engage in activities you enjoy."
            ]

        return recommendations