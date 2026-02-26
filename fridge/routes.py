from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.security import get_current_user
from app.utils.db import get_session
from auth.models import User
from fridge.models import Fridge
from fridge.schemas import FridgeDetails

fridge_router = APIRouter(prefix="/fridge", tags=["fridge"])


@fridge_router.get("/fridge", response_model=FridgeDetails, status_code=200)
async def get_fridge(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    result = await session.scalars(
        select(Fridge).where(Fridge.user_id == user.id).options(selectinload(Fridge.products))
    )
    fridge = result.first()
    return fridge


@fridge_router.post("products")
async def add_products():
    pass


@fridge_router.get("expired")
async def get_expired_products():
    pass


@fridge_router.delete("expired")
async def delete_expired_products():
    pass
