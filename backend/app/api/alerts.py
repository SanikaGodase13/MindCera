from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.alert import Alert

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    alerts = (
        db.query(Alert)
        .filter(Alert.user_id == current_user.id)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "conversation_id": a.conversation_id,
            "risk_level": a.risk_level,
            "message": a.message,
            "status": a.status,
            "created_at": a.created_at
        }
        for a in alerts
    ]

@router.patch("/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.user_id == current_user.id
        )
        .first()
    )

    if not alert:

        return {
            "error": "Alert not found"
        }

    alert.status = "RESOLVED"

    db.commit()

    return {
        "message": "Alert resolved successfully"
    }