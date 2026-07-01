from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import Counter

from app.database.db import get_db
from app.models.emotion_log import EmotionLog
from app.core.dependencies import get_current_user
from app.models.user import User
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    logs = (
            db.query(EmotionLog)
            .filter(
                EmotionLog.user_id == current_user.id
            )
            .all()
    )

    if not logs:
        return {
            "message": "No analysis data found"
        }

    # --------------------
    # Emotion Statistics
    # --------------------

    emotions = [
        log.dominant_emotion
        for log in logs
    ]

    emotion_counts = Counter(emotions)

    dominant_emotion = emotion_counts.most_common(1)[0][0]

    # --------------------
    # Risk Statistics
    # --------------------

    high_count = sum(
        1 for log in logs
        if log.risk_level == "HIGH"
    )

    medium_count = sum(
        1 for log in logs
        if log.risk_level == "MEDIUM"
    )

    low_count = sum(
        1 for log in logs
        if log.risk_level == "LOW"
    )

    # --------------------
    # Wellness Score
    # --------------------

    score_map = {
        "LOW": 100,
        "MEDIUM": 60,
        "HIGH": 20
    }

    scores = [
        score_map.get(log.risk_level, 50)
        for log in logs
    ]

    wellness_score = round(
        sum(scores) / len(scores),
        2
    )

    return {
        "total_entries": len(logs),
        "dominant_emotion": dominant_emotion,
        "emotion_distribution": emotion_counts,
        "risk_distribution": {
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        },
        "wellness_score": wellness_score
    }

@router.get("/trends")
def get_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    logs = (
        db.query(EmotionLog)
        .filter(
            EmotionLog.user_id == current_user.id,
            EmotionLog.created_at >= seven_days_ago
        )
        .all()
    )

    if not logs:
        return {
            "message": "No trend data available"
        }

    emotions = [
        log.dominant_emotion
        for log in logs
    ]

    emotion_counts = Counter(emotions)

    dominant_emotion = (
        emotion_counts.most_common(1)[0][0]
    )

    fear_count = emotion_counts.get("fear", 0)
    sad_count = emotion_counts.get("sadness", 0)

    negative_count = fear_count + sad_count

    total_entries = len(logs)

    negative_ratio = negative_count / total_entries

    if negative_ratio >= 0.7:
        stress_indicator = "HIGH"

    elif negative_ratio >= 0.4:
        stress_indicator = "MEDIUM"

    else:
        stress_indicator = "LOW"

    return {
        "entries_last_7_days": total_entries,
        "dominant_emotion": dominant_emotion,
        "emotion_counts": dict(emotion_counts),
        "stress_indicator": stress_indicator
    }

@router.get("/report")
def get_report(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    start_date = (
        datetime.now(timezone.utc)
        - timedelta(days=days)
    )

    logs = (
        db.query(EmotionLog)
        .filter(
            EmotionLog.user_id == current_user.id,
            EmotionLog.created_at >= start_date
        )
        .order_by(EmotionLog.created_at.asc())
        .all()
    )

    if not logs:
        return {
            "message": f"No data available for the last {days} days"
        }

    # --------------------
    # Emotion Statistics
    # --------------------

    emotions = [
        log.dominant_emotion
        for log in logs
    ]

    emotion_counts = Counter(emotions)

    dominant_emotion = (
        emotion_counts.most_common(1)[0][0]
    )

    # --------------------
    # Risk Distribution
    # --------------------

    high_count = sum(
        1 for log in logs
        if log.risk_level == "HIGH"
    )

    medium_count = sum(
        1 for log in logs
        if log.risk_level == "MEDIUM"
    )

    low_count = sum(
        1 for log in logs
        if log.risk_level == "LOW"
    )

    # --------------------
    # Wellness Score
    # --------------------

    score_map = {
        "LOW": 100,
        "MEDIUM": 60,
        "HIGH": 20
    }

    wellness_scores = [
        score_map.get(log.risk_level, 50)
        for log in logs
    ]

    average_wellness_score = round(
        sum(wellness_scores)
        / len(wellness_scores),
        2
    )

    # --------------------
    # Stress Indicator
    # --------------------

    fear_count = emotion_counts.get("fear", 0)
    sad_count = emotion_counts.get("sadness", 0)

    negative_count = (
        fear_count + sad_count
    )

    negative_ratio = (
        negative_count / len(logs)
    )

    if negative_ratio >= 0.7:
        stress_indicator = "HIGH"

    elif negative_ratio >= 0.4:
        stress_indicator = "MEDIUM"

    else:
        stress_indicator = "LOW"

    # --------------------
    # Wellness Trend
    # --------------------

    midpoint = len(wellness_scores) // 2

    first_half = wellness_scores[:midpoint]
    second_half = wellness_scores[midpoint:]

    if first_half and second_half:

        first_avg = (
            sum(first_half)
            / len(first_half)
        )

        second_avg = (
            sum(second_half)
            / len(second_half)
        )

        if second_avg > first_avg + 10:
            wellness_trend = "IMPROVING"

        elif second_avg < first_avg - 10:
            wellness_trend = "DECLINING"

        else:
            wellness_trend = "STABLE"

    else:
        wellness_trend = "INSUFFICIENT_DATA"

    # --------------------
    # Summary
    # --------------------

    if stress_indicator == "HIGH":

        summary = (
            "Persistent negative emotions detected. "
            "Consider prioritizing self-care and support."
        )

    elif stress_indicator == "MEDIUM":

        summary = (
            "Moderate emotional stress observed. "
            "Monitor emotional patterns regularly."
        )

    else:

        summary = (
            "Overall emotional state appears stable."
        )

    return {
        "period_days": days,
        "total_entries": len(logs),
        "average_wellness_score": average_wellness_score,
        "dominant_emotion": dominant_emotion,
        "emotion_distribution": dict(emotion_counts),
        "risk_distribution": {
            "HIGH": high_count,
            "MEDIUM": medium_count,
            "LOW": low_count
        },
        "stress_indicator": stress_indicator,
        "wellness_trend": wellness_trend,
        "summary": summary
    }