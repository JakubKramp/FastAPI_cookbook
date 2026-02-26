from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.db import Base


class Fridge(Base):
    """
    Model that reflects the produce an user currently have in their fridge.
    Relations:
    - User (auth) one to one
    - Product (recipes) one to many
    """

    __tablename__ = "fridge"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        back_populates="fridge",
        lazy="selectin",
        uselist=True,
    )
    products: Mapped[List["Product"]] = relationship(
        back_populates="fridge",
        lazy="selectin",
        uselist=True,
    )
