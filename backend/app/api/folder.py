from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.monitored_folder import MonitoredFolder
from app.models.user import User
from app.core.dependencies import get_current_user

from app.schemas.folder import FolderCreate
from app.services.folder_analyzer import FolderAnalyzer
from app.services.sentiment_service import SentimentService
from app.services.emotion_service import EmotionService

from app.core.risk_engine import RiskEngine
from app.core.recommendation_engine import RecommendationEngine

from app.models.emotion_log import EmotionLog
from app.services.folder_watcher import FolderWatcher
from app.services.watcher_registry import active_watchers


folder_analyzer = FolderAnalyzer()

sentiment_service = SentimentService()
emotion_service = EmotionService()

risk_engine = RiskEngine()
recommendation_engine = RecommendationEngine()

router = APIRouter(
    prefix="/folder",
    tags=["Folder Monitoring"]
)


@router.post("/register")
def register_folder(
    folder: FolderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_folder = MonitoredFolder(
        user_id=current_user.id,
        folder_name=folder.folder_name,
        folder_path=folder.folder_path
    )

    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    return {
        "message": "Folder registered successfully",
        "folder_id": new_folder.id
    }


@router.get("/")
def get_folders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    folders = (
        db.query(MonitoredFolder)
        .filter(
            MonitoredFolder.user_id == current_user.id
        )
        .all()
    )

    return folders


@router.get("/test/{folder_id}")
def test_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    folder = (
        db.query(MonitoredFolder)
        .filter(
            MonitoredFolder.id == folder_id,
            MonitoredFolder.user_id == current_user.id
        )
        .first()
    )

    if not folder:
        return {
            "error": "Folder not found"
        }

    text = (
        folder_analyzer
        .extract_text_from_folder(
            folder.folder_path
        )
    )

    return {
        "combined_text": text
    }

@router.post("/analyze/{folder_id}")
def analyze_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    folder = (
        db.query(MonitoredFolder)
        .filter(
            MonitoredFolder.id == folder_id,
            MonitoredFolder.user_id == current_user.id
        )
        .first()
    )

    if not folder:
        return {
            "error": "Folder not found"
        }

    combined_text = (
        folder_analyzer.extract_text_from_folder(
            folder.folder_path
        )
    )

    if not combined_text.strip():
        return {
            "error": "No text files found"
        }

    sentiment_result = (
        sentiment_service.predict(
            combined_text
        )
    )

    emotion_result = (
        emotion_service.predict(
            combined_text
        )
    )

    risk_level = (
        risk_engine.assess_risk(
            sentiment_result["sentiment"],
            emotion_result["dominant_emotion"]
        )
    )

    recommendations = (
        recommendation_engine.get_recommendations(
            risk_level,
            emotion_result["dominant_emotion"]
        )
    )

    emotion_score = (
        emotion_result["scores"][
            emotion_result["dominant_emotion"]
        ]
    )

    log = EmotionLog(
        user_id=current_user.id,
        message=combined_text,
        sentiment=sentiment_result["sentiment"],
        sentiment_confidence=sentiment_result["confidence"],
        dominant_emotion=emotion_result["dominant_emotion"],
        emotion_score=emotion_score,
        risk_level=risk_level
    )

    db.add(log)
    db.commit()

    return {
        "folder_name": folder.folder_name,
        "sentiment": sentiment_result,
        "emotion": emotion_result,
        "risk_level": risk_level,
        "recommendations": recommendations
    }


@router.post("/start-monitoring/{folder_id}")
def start_monitoring(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    folder = (
        db.query(MonitoredFolder)
        .filter(
            MonitoredFolder.id == folder_id,
            MonitoredFolder.user_id == current_user.id
        )
        .first()
    )

    if not folder:
        return {
            "error": "Folder not found"
        }

    if folder_id in active_watchers:
        return {
            "message": "Already monitoring"
        }

    watcher = FolderWatcher()

    watcher.start(
        folder_id,
        folder.folder_path
    )

    active_watchers[folder_id] = watcher

    return {
        "message": "Monitoring started"
    }

@router.post("/stop-monitoring/{folder_id}")
def stop_monitoring(
    folder_id: int
):

    watcher = active_watchers.get(folder_id)

    if not watcher:
        return {
            "message": "Watcher not running"
        }

    watcher.stop()

    del active_watchers[folder_id]

    return {
        "message": "Monitoring stopped"
    }