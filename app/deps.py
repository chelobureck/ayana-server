from fastapi import Header, HTTPException, status
from .config import settings
import jwt

async def get_current_user_uid(authorization: str | None = Header(default=None)) -> str:
    # Expect Authorization: Bearer <token>
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    # For MVP: trust token is a signed JWT with claim 'uid' OR just a raw uid in dev
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        uid = payload.get("uid")
        if not uid:
            raise ValueError("uid missing")
        return uid
    except Exception:
        # dev fallback: allow raw uid token if DEBUG
        if settings.APP_DEBUG and token:
            return token
        raise HTTPException(status_code=401, detail="Invalid token") 