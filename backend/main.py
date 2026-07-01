from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import engine
from app.database.base import Base

import app.models.user
import app.models.password_reset_otp
import app.models.emotion_log   # <-- ADD THIS

from app.api.auth import router as auth_router
from app.api.analyze import router as analyze_router
from app.api.history import router as history_router
from app.api.analytics import router as analytics_router
import app.models.monitored_folder
from app.api.folder import router as folder_router

from app.models.chat_conversation import ChatConversation
from app.models.chat_message import ChatMessage
from app.api.chat import router as chat_router
import app.models.alert
from app.api.alerts import router as alerts_router
from app.api.dashboard import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindCera API",
    version="1.0.0"
)

app.add_middleware(
CORSMiddleware,


allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500"
],

allow_credentials=True,

allow_methods=["*"],

allow_headers=["*"]


)


app.include_router(auth_router)
app.include_router(analyze_router)
app.include_router(history_router)
app.include_router(analytics_router)
app.include_router(folder_router)
app.include_router(chat_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to MindCera API"
    }