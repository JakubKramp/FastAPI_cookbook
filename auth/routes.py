from datetime import timedelta

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, create_engine, select
from passlib.context import CryptContext
from starlette import status

from app.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_username,
)
from auth.schemas import Token
from config import settings
from auth.models import User, UserDetail

engine = create_engine(settings.DATABASE_URL, echo=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_session():
    with Session(engine) as session:
        yield session


user_router = APIRouter(prefix="/user", tags=["auth"])


@user_router.post("/", response_model=UserDetail, status_code=201)
def sign_up(user: UserDetail, session: Session = Depends(get_session)):
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    return db_user


@user_router.get("/", response_model=UserDetail, status_code=200)
def user_detail(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/me", response_model=UserDetail, status_code=200)
def current_user(
    session: Session = Depends(get_session), user: str = Depends(get_current_username)
):
    authenticated_user = session.scalars(
        select(User).where(User.username == user)
    ).first()
    return authenticated_user


@user_router.patch("/", response_model=UserDetail)
def update_user(
    user_id: int, user_data: UserDetail, session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_data.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@user_router.delete("/")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {f"User {user_id} deleted"}


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
