from fastapi import Header, HTTPException, status, Depends
from typing import Optional

from .security import decode_token
from .database import get_db
from sqlalchemy.orm import Session
from .models import User


class AuthContext:
    def __init__(self, user_id: Optional[int], access_level: int):
        self.user_id = user_id
        self.access_level = access_level


def get_auth_context(authorization: Optional[str] = Header(default=None)) -> AuthContext:
    """
    Bearer JWT only.
    - Authorization: Bearer <jwt>
    """
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        decoded = decode_token(token)
        if not decoded:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user_id, level = decoded
        return AuthContext(user_id=user_id, access_level=level)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")


def require_access(min_level: int):
    def dependency(ctx: AuthContext = Depends(get_auth_context), db: Session = Depends(get_db)) -> AuthContext:
        # Refresh access level from DB if user_id is present to honor runtime changes
        effective_level = ctx.access_level
        if ctx.user_id is not None:
            user = db.get(User, ctx.user_id)
            if user is not None and isinstance(user.access_level, int):
                effective_level = user.access_level
        if effective_level < min_level:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient access level")
        ctx.access_level = effective_level
        return ctx
    return dependency
