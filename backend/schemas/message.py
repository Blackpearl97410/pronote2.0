from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    recipient_id: int
    subject: str
    body: str


class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    subject: str
    body: str
    is_read: bool
    sent_at: datetime
    read_at: Optional[datetime]

    model_config = {"from_attributes": True}
