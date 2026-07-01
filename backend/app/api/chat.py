from fastapi import APIRouter

from app.models.alert import Alert

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.models.user import User
from app.models.chat_conversation import ChatConversation

from app.core.dependencies import get_current_user

from app.models.chat_message import ChatMessage

from app.schemas.chat import ChatSendRequest

from app.services.chat_service import ChatService
from app.services.gemini_service import GeminiService
from app.core.recommendation_engine import RecommendationEngine
from app.services.guardrail_service import GuardrailService
from app.core.crisis_detector import CrisisDetector
from app.services.email_service import (
    send_guardian_alert
)

chat_service = ChatService()
gemini_service = GeminiService()
recommendation_engine = RecommendationEngine()
guardrail_service = GuardrailService()
crisis_detector = CrisisDetector()

@router.post("/conversation")
def create_conversation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = ChatConversation(
        user_id=current_user.id,
        title="Wellness Chat"
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return {
        "conversation_id": conversation.id
    }

@router.post("/send")
def send_message(
    data: ChatSendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ----------------------
    # Find Conversation
    # ----------------------

    conversation = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.id == data.conversation_id,
            ChatConversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:

        return {
            "error": "Conversation not found"
        }

    # ----------------------
    # Previous Messages
    # ----------------------

    previous_messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.conversation_id == conversation.id
        )
        .order_by(ChatMessage.id.desc())
        .limit(10)
        .all()
    )

    conversation_history = ""

    for msg in reversed(previous_messages):

        conversation_history += (
            f"{msg.role}: {msg.message}\n"
        )

    # ----------------------
    # Analyze User Message
    # ----------------------

    analysis = (
        chat_service.analyze_message(
            data.message
        )
    )

    # ----------------------
    # Crisis Detection Override
    # ----------------------

    if crisis_detector.is_high_risk(
        data.message
    ):
        analysis["risk"] = "HIGH"

    recommendations = (
        recommendation_engine.get_recommendations(
            analysis["risk"],
            analysis["emotion"]["dominant_emotion"]
        )
    )

    # ----------------------
    # Save User Message
    # ----------------------

    user_message = ChatMessage(
        conversation_id=conversation.id,
        role="user",
        message=data.message,
        sentiment=analysis["sentiment"]["sentiment"],
        emotion=analysis["emotion"]["dominant_emotion"],
        risk_level=analysis["risk"]
    )

    db.add(user_message)

    # ----------------------
    # High Risk Alert
    # ----------------------

    if analysis["risk"] == "HIGH":

        alert = Alert(
            user_id=current_user.id,
            conversation_id=conversation.id,
            risk_level="HIGH",
            message=data.message,
            status="ACTIVE"
        )

        db.add(alert)

        if current_user.guardian_email:

            try:

                send_guardian_alert(
                    guardian_email=current_user.guardian_email,
                    user_name=current_user.name,
                    risk_level="HIGH"
                )

                print(
                    f"Guardian alert email sent to "
                    f"{current_user.guardian_email}"
                )

            except Exception as e:

                print(
                    f"Guardian email failed: {e}"
                )

    # ----------------------
    # Gemini Response
    # ----------------------

    if not guardrail_service.is_wellness_related(
        data.message
    ):

        ai_reply = (
            "I am a wellness-focused companion. "
            "I can help with emotional wellbeing, stress, "
            "anxiety, self-reflection, and healthy habits."
        )

    else:

        ai_reply = gemini_service.generate_response(
            user_message=data.message,
            conversation_history=conversation_history
        )

    # ----------------------
    # Save AI Message
    # ----------------------

    ai_message = ChatMessage(
        conversation_id=conversation.id,
        role="assistant",
        message=ai_reply
    )

    db.add(ai_message)

    db.commit()

    print("AI REPLY =", ai_reply)

    return {
        "conversation_id": conversation.id,
        "analysis": analysis,
        "recommendations": recommendations,
        "ai_response": ai_reply
    }

@router.get("/history/{conversation_id}")
def get_chat_history(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.id == conversation_id,
            ChatConversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:

        return {
            "error": "Conversation not found"
        }

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.conversation_id == conversation_id
        )
        .order_by(ChatMessage.id.asc())
        .all()
    )

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "message": msg.message,
                "sentiment": msg.sentiment,
                "emotion": msg.emotion,
                "risk_level": msg.risk_level,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

@router.get("/conversations")
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversations = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.user_id == current_user.id
        )
        .order_by(
            ChatConversation.id.desc()
        )
        .all()
    )

    return {
        "conversations": [
            {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at
            }
            for conversation in conversations
        ]
    }