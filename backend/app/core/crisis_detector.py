class CrisisDetector:

    HIGH_RISK_PHRASES = [

        "suicide",
        "kill myself",
        "want to die",
        "end my life",
        "self harm",
        "hurt myself",
        "nothing matters anymore",
        "life is meaningless",
        "i want to disappear",
        "i give up",
        "i can't go on"

    ]

    def is_high_risk(self, text: str):

        text = text.lower()

        for phrase in self.HIGH_RISK_PHRASES:

            if phrase in text:
                return True

        return False