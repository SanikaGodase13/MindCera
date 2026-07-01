import os
from datetime import datetime, timezone

from app.models.emotion_log import EmotionLog

from app.services.folder_analyzer import FolderAnalyzer
from app.services.sentiment_service import SentimentService
from app.services.emotion_service import EmotionService

from app.core.risk_engine import RiskEngine


class FolderProcessor:

    def __init__(self):

        self.folder_analyzer = FolderAnalyzer()
        self.sentiment_service = SentimentService()
        self.emotion_service = EmotionService()

        self.risk_engine = RiskEngine()

    def process_folder(
        self,
        folder,
        db
    ):

        current_file_count = len(
            [
                f for f in os.listdir(folder.folder_path)
                if f.lower().endswith(
                    (".txt", ".docx", ".pdf")
                )
            ]
        )

        if current_file_count <= folder.last_file_count:
            print(
                f"No new files detected for folder {folder.id}"
            )
            return

        folder.last_file_count = current_file_count

        text = self.folder_analyzer.extract_text_from_folder(
            folder.folder_path
        )

        if not text.strip():
            print(
                f"No text found in folder {folder.id}"
            )
            return

        sentiment_result = (
            self.sentiment_service.predict(text)
        )

        emotion_result = (
            self.emotion_service.predict(text)
        )

        risk_level = (
            self.risk_engine.assess_risk(
                sentiment_result["sentiment"],
                emotion_result["dominant_emotion"]
            )
        )

        emotion_score = (
            emotion_result["scores"][
                emotion_result["dominant_emotion"]
            ]
        )

        log = EmotionLog(
            user_id=folder.user_id,
            message=text,
            sentiment=sentiment_result["sentiment"],
            sentiment_confidence=sentiment_result["confidence"],
            dominant_emotion=emotion_result["dominant_emotion"],
            emotion_score=emotion_score,
            risk_level=risk_level
        )

        db.add(log)

        folder.last_scanned_at = datetime.now(
            timezone.utc
        )

        db.commit()

        print(
            f"Folder {folder.id} processed successfully"
        )

    def process_file(
        self,
        folder,
        file_path,
        db
    ):

        text = (
            self.folder_analyzer
            .extract_text_from_file(file_path)
        )

        if not text.strip():
            return

        sentiment_result = (
            self.sentiment_service.predict(text)
        )

        emotion_result = (
            self.emotion_service.predict(text)
        )

        risk_level = (
            self.risk_engine.assess_risk(
                sentiment_result["sentiment"],
                emotion_result["dominant_emotion"]
            )
        )

        emotion_score = (
            emotion_result["scores"][
                emotion_result["dominant_emotion"]
            ]
        )

        log = EmotionLog(
            user_id=folder.user_id,
            message=text,
            sentiment=sentiment_result["sentiment"],
            sentiment_confidence=sentiment_result["confidence"],
            dominant_emotion=emotion_result["dominant_emotion"],
            emotion_score=emotion_score,
            risk_level=risk_level
        )

        db.add(log)

        folder.last_scanned_at = datetime.now(
            timezone.utc
        )

        db.commit()

        print(
            f"Processed file: {file_path}"
        )