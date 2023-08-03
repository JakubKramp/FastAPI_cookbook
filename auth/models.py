from typing import Optional

from sqlalchemy import String, Column
from sqlalchemy.event import listens_for
from sqlmodel import Field, SQLModel, Relationship

from scrap import Scrapper


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all,delete,delete-orphan",
        },
    )


class UserList(SQLModel):
    id: int
    email: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "username": "jeffS",
            }
        }


class UserUpdate(SQLModel):
    email: str | None
    username: str | None
    password: str | None

    class Config:
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }


class UserCreate(UserList):
    password: str | None

    class Config:
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }


class UpdateProfile(SQLModel):
    sex: str | None
    activity_factor: str | None
    age: int | None
    height: int | None
    weight: int | None
    smoking: bool | None


class BaseProfile(SQLModel):
    sex: str
    activity_factor: str | None
    age: int
    height: int
    weight: int
    smoking: bool


class DietaryReferenceIntakes(SQLModel):
    calories: int | None
    carbohydrates: int | None
    fat: int | None
    protein: int | None
    fiber: int | None
    potassium: int | None
    sodium: int | None


class Profile(BaseProfile, DietaryReferenceIntakes, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"uselist": False},
    )
    user_id: int | None = Field(default=None, foreign_key="user.id")

    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "age": 30,
                "height": 180,
                "weight": 80,
                "activity_factor": "Little/no exercise",
                "smoking": True,
            }
        }


@listens_for(Profile, "before_insert")
def set_dietary_reference_intakes(mapper, connection, target):
    Scrapper.get_DRI(target)


class UserDetail(UserList):
    profile: Profile | None
