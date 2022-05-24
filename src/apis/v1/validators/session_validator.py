import uuid
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID

class SessionSerializer(BaseModel):
    cookie_id: uuid.UUID
    user_id: str

# x = SessionSerializer(cookie_id="f8a8705b-d09c-4a37-9ad4-6f5d7c6b2798", user_id="123")