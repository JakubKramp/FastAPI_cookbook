from datetime import date

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from recipes.models import Product
from recipes.tests.test_data.example_data import example_db_product


@pytest_asyncio.fixture(name="expired_product")
async def expired_product(user: User, session: AsyncSession) -> Product:
    product = await Product.create(session, **example_db_product, marked_for_delete=True)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@pytest_asyncio.fixture(name="product")
async def product(user: User, session: AsyncSession) -> Product:
    product = await Product.create(session, **example_db_product, marked_for_delete=False)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
