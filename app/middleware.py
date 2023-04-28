from jose import jwt
from sqlmodel import Session, select
from starlette.authentication import AuthenticationBackend, AuthCredentials

from app.utils.db import engine, get_session
from auth.models import User
from config import settings


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "authorization" not in conn.headers:
            return

        auth = conn.headers["authorization"]
        token_type, token = auth.split()
        if token_type == "Bearer":
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
        else:
            return
        session = get_session()
        user = session.scalars(select(User).where(User.username == username)).first()

        return AuthCredentials(["authenticated"]), user
