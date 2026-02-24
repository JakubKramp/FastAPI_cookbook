from datetime import timedelta

from fastapi import APIRouter, Response, BackgroundTasks
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from starlette import status

from app.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
)
from auth.schemas import Token, UserDetail, UserCreate, UserUpdate, ProfileDetail, UserList, BaseProfile
from config import settings
from auth.models import (
    User,
    Profile,

)
from app.utils.db import get_session
from scrap import DRIClient

user_router = APIRouter(prefix="/user", tags=["auth"])


@user_router.post("/", response_model=UserList, status_code=201)
async def sign_up(user: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    try:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username/email already taken")
    return db_user


@user_router.get("/", response_model=UserDetail, status_code=200)
async def user_detail(user_id: int, session: AsyncSession = Depends(get_session)) -> User:
    user = await session.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    user = user.scalar_one()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("/me", response_model=UserDetail, status_code=200)
async def current_user(user: User = Depends(get_current_user)) -> User:
    return user


@user_router.patch("/", response_model=UserDetail)
async def update_user(
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> User:
    user_data = user_data.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        if key == "password":
            value = get_password_hash(value)
        setattr(user, key, value)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@user_router.delete("/", status_code=204)
async def delete_user(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)) -> Response:
    await session.delete(user)
    await session.commit()
    return Response(status_code=204, content=f"User {user.id} deleted")


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/profile", response_model=ProfileDetail, status_code=201)
async def create_user_profile(
        profile: BaseProfile,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user),
):
    result = await session.scalars(select(Profile).where(Profile.user_id == user.id))
    if db_profile := result.first():
        return db_profile
    db_profile = Profile(**profile.model_dump(), user_id=user.id)
    session.add(db_profile)
    dri_client = DRIClient()
    background_tasks.add_task(dri_client.fill_profile,db_profile, session)
    await session.commit()
    await session.refresh(db_profile)
    return db_profile

"""
@user_router.patch("/profile", response_model=Profile, status_code=200)
async def update_user_profile(
    profile_data: UpdateProfile,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    profile = session.scalars(
        select(Profile, User).join(Profile.user).where(User == user)
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
"""