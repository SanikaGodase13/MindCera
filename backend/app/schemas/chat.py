from pydantic import BaseModel


class ChatSendRequest(BaseModel):

    conversation_id: int

    message: str