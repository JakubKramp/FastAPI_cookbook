from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from app.utils.db import get_session
from auth.dri_scrapper import DRIClient
from auth.exceptions import credentials_exception
from auth.models import (
    Profile,
    User,
)
from auth.schemas import (
    BaseProfile,
    ProfileDetail,
    Token,
    UpdateProfile,
    UserCreate,
    UserDetail,
    UserList,
    UserUpdate,
)
from config import settings

user_router = APIRouter(prefix="/user", tags=["auth"])


@user_router.post("/", response_model=UserList, status_code=201)
async def sign_up(user: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    """
    Creates new user. \n
    Return status code: \n
    201 - Successfully created a user \n
    409 - Username/email is taken.
    """
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


@user_router.get("/me", response_model=UserDetail, status_code=200)
async def current_user(user: User = Depends(get_current_user)) -> User:
    """
    Returns data about currently logged-in user.
    Note that it has to be higher than user-detail, because of route resolution order. \n
    Return status code: \n
    200 - Successfully returned user data \n
    401 - User not authenticated
    """
    print(user)
    return user


@user_router.get("/{user_id}", response_model=UserDetail, status_code=200)
async def user_detail(user_id: int, session: AsyncSession = Depends(get_session)) -> User:
    """
    Returns data about user with given id. \n
    Return status code: \n
    200 - Successfully returned user data \n
    404 - User not found
    """
    user = await session.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.patch("/", response_model=UserDetail)
async def update_user(
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> User:
    """
    Update currently logged-in user. \n
    Return status code: \n
    200 - Successfully updated user \n
    401 - User not authenticated
    """
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
    """
    Delete currently logged-in user.
    Return status code:
    204 - Successfully deleted user
    401 - User not authenticated
    """
    await session.delete(user)
    await session.commit()
    return Response(content='', status_code=204)


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns JWT access token.
    Return status code:
    200 - Successfully logged in user
    401 - Invalid credentials
    """
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise credentials_exception
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
    """
    Creates user profile for current user.
    If playwright is installed DRI data will be automatically scrapped via a background task.
    Return status code:
    201 - Successfully created user profile
    401 - User not authenticated
    """
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


@user_router.patch("/profile", response_model=ProfileDetail, status_code=200)
async def update_user_profile(
    profile_data: UpdateProfile,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """
    Updates user profile for current user.
    Updating profile does not affect the DRI.
    Return status code:
    200 - Successfully updated user
    401 - User not authenticated
    """
    result = await session.scalars(select(Profile).where(Profile.user_id == user.id))
    profile = result.first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile
