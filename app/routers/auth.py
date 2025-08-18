from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..models import User
from ..config import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/ensure-user")
async def ensure_user(uid: str, display_name: str | None = None, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.uid == uid))
    user = q.scalar_one_or_none()
    if user is None:
        user = User(uid=uid, display_name=display_name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return {"user_id": user.id} 


@router.post("/google")
async def login_with_google(id_token_str: str, db: AsyncSession = Depends(get_db)):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID is not configured")

    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
        if idinfo.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
            raise ValueError("Wrong issuer")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google ID token")

    google_sub = idinfo.get("sub")
    email = idinfo.get("email")
    name = idinfo.get("name")
    if not google_sub:
        raise HTTPException(status_code=401, detail="Invalid Google payload")

    # Use stable UID namespace for Google users
    uid = f"google:{google_sub}"

    q = await db.execute(select(User).where(User.uid == uid))
    user = q.scalar_one_or_none()
    if user is None:
        user = User(uid=uid, display_name=name or email)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Issue our app JWT for simplicity
    token_payload = {"uid": uid}
    app_token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    return {"access_token": app_token, "token_type": "bearer", "user_id": user.id}