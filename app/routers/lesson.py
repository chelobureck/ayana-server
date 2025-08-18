from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..models import User, ChatSession, Message
from ..schemas import TurnRequest, TurnReply, CreateSessionRequest, CreateSessionReply
from ..ai import orchestrate_turn

router = APIRouter(prefix="/lesson", tags=["lesson"])

@router.post("/create-session", response_model=CreateSessionReply)
async def create_session(body: CreateSessionRequest, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.uid == body.user_uid))
    user = q.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session = ChatSession(user_id=user.id, topic=body.topic)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return CreateSessionReply(session_id=session.id)

@router.post("/turn", response_model=TurnReply)
async def turn(body: TurnRequest, db: AsyncSession = Depends(get_db)):
    # ensure user
    q = await db.execute(select(User).where(User.uid == body.user_uid))
    user = q.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # ensure/create session
    if body.session_id is None:
        cs = ChatSession(user_id=user.id, topic=body.topic)
        db.add(cs)
        await db.commit()
        await db.refresh(cs)
        session_id = cs.id
    else:
        session_id = body.session_id

    # persist incoming messages
    dialog = []
    for m in body.messages:
        db.add(Message(session_id=session_id, role=m.role, content=m.content))
        dialog.append({"role": m.role, "content": m.content})
    await db.commit()

    # orchestrate LLM
    reply = await orchestrate_turn(dialog)

    # store reply
    db.add(Message(session_id=session_id, role=reply.get("role", "system"), content=reply.get("say", ""), meta={"animations": reply.get("animations"), "next_task": reply.get("next_task")}))
    await db.commit()

    return TurnReply(**{
        "role": reply.get("role", "system"),
        "say": reply.get("say", ""),
        "animations": reply.get("animations", []),
        "next_task": reply.get("next_task"),
    }) 