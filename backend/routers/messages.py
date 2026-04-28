from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.message import Message
from backend.schemas.message import MessageCreate, MessageOut

router = APIRouter(prefix="/api/messages", tags=["Messagerie"])


@router.get("/inbox", response_model=List[MessageOut])
async def get_inbox(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Message)
        .where(Message.recipient_id == current_user["user_id"])
        .order_by(Message.sent_at.desc())
    )
    return result.scalars().all()


@router.get("/sent", response_model=List[MessageOut])
async def get_sent(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Message)
        .where(Message.sender_id == current_user["user_id"])
        .order_by(Message.sent_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=MessageOut)
async def send_message(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    msg = Message(**payload.model_dump(), sender_id=current_user["user_id"])
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


@router.patch("/{message_id}/read", response_model=MessageOut)
async def mark_as_read(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(select(Message).where(Message.id == message_id))
    msg = result.scalar_one_or_none()
    if not msg or msg.recipient_id != current_user["user_id"]:
        raise HTTPException(status_code=404, detail="Message introuvable")
    msg.is_read = True
    msg.read_at = datetime.utcnow()
    await db.commit()
    await db.refresh(msg)
    return msg
