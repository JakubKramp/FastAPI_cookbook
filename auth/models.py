from typing import Optional

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlmodel import Field, SQLModel, Relationship

from app.utils.db import Base
from auth.schemas import DietaryReferenceIntakes, BaseProfile


#from scrap import Scrapper


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(250), unique=True)

    addresses: Mapped["Profile"] = relationship(
     back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.email!r})"




class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)

    # BaseProfile
    sex: Mapped[str] = mapped_column(String)
    activity_factor: Mapped[str | None] = mapped_column(String)
    age: Mapped[int] = mapped_column()
    height: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()
    smoking: Mapped[bool] = mapped_column()

    # DietaryReferenceIntakes
    calories: Mapped[int | None] = mapped_column()
    carbohydrates: Mapped[int | None] = mapped_column()
    fat: Mapped[int | None] = mapped_column()
    protein: Mapped[int | None] = mapped_column()
    fiber: Mapped[int | None] = mapped_column()
    potassium: Mapped[int | None] = mapped_column()
    sodium: Mapped[int | None] = mapped_column()

    # Relationship
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), default=None)
    user: Mapped["User | None"] = relationship(
        back_populates="profile",
        uselist=False,
    )


@listens_for(Profile, "before_insert")
def set_dietary_reference_intakes(mapper, connection, target):
    pass
    #Scrapper.get_DRI(target)

