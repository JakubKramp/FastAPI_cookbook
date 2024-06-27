from datetime import timedelta

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from starlette import status

from app.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
)
from auth.schemas import Token
from config.settings import Settings
from auth.models import (
    User,
    UserDetail,
    Profile,
    UserCreate,
    UpdateProfile,
    UserUpdate, UserList,
)
from app.utils.db import get_session

user_router = APIRouter(prefix="/user", tags=["auth"])


@user_router.post("/", response_model=UserDetail, status_code=201)
def sign_up(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    try:
        session.add(db_user)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username/email already taken")
    return db_user


@user_router.get("/", response_model=UserDetail, status_code=200)
def user_detail(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/me", response_model=UserDetail, status_code=200)
def current_user(session: Session = Depends(get_session), user: str = Depends(get_current_user)):
    authenticated_user = session.scalars(select(User).where(User.id == int(user))).first()
    return authenticated_user


@user_router.patch("/", response_model=UserList)
def update_user(
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    user: str = Depends(get_current_user),
):
    user = session.scalars(select(User).where(User.id == int(user))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_data.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        if key == "password":
            value = get_password_hash(value)
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@user_router.delete("/", status_code=204)
def delete_user(session: Session = Depends(get_session), user: str = Depends(get_current_user)):
    user = session.scalars(select(User).where(User.username == user)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {f"User {user.id} deleted"}


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
    access_token_expires = timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/profile", response_model=Profile, status_code=201)
async def create_user_profile(
    profile: Profile,
    session: Session = Depends(get_session),
    user: str = Depends(get_current_user),
):
    user = session.scalars(select(User).where(User == user)).first()
    if db_profile := session.scalars(select(Profile).where(Profile.user == user)).first():
        return db_profile
    profile.user_id = user.id
    session.add(profile)
    session.commit()
    return profile


@user_router.patch("/profile", response_model=Profile, status_code=200)
async def update_user_profile(
    profile_data: UpdateProfile,
    session: Session = Depends(get_session),
    username: str = Depends(get_current_user),
):
    profile = session.scalars(
        select(Profile, User).join(Profile.user).where(User.username == username)
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    profile_data = profile_data.dict(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(profile, key, value)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
