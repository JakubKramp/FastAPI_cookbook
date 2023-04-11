from sqlalchemy import String, Column, Enum
from sqlmodel import Field, SQLModel, Relationship

from auth.enums import Sex, ActivityFactor


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str


class UserDetail(SQLModel):
    email: str
    password: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "email": "jeff.spicoli@labeouf.com",
                "password": "hewillnotdivideus",
                "username": "jeffS",
            }
        }


class UserList(SQLModel):
    id: int
    email: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "jeff.spicoli@labeouf.com",
                "username": "jeffS",
            }
        }


class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sex: Sex = Field(sa_column=Column(Enum(Sex)))
    activity_factor: ActivityFactor = Field(sa_column=Column(Enum(ActivityFactor)))
    age: int
    height: int
    wight: int
    smoking: bool
    user: User | None = Relationship(back_populates="profile")
    user_id: int | None = Field(default=None, foreign_key="user.id")

    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "age": 30,
                "height": 180,
                "wieght": 80,
                "activity_factor": "Little/no excercise",
                "smoking": True,
            }
        }


class DietaryReferenceIntakes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    calories: int
    carbohydrates: int
    fat: int
    protein: int
    fiber: int
    potassium: int
    sodium: int
    user: User | None = Relationship(back_populates="DRI")
    user_id: int | None = Field(default=None, foreign_key="user.id")

    class Config:
        schema_extra = {
            "example": {
                "calories": 2000,
                "carbohydrates": 200,
                "fat": 50,
                "protein": 70,
                "fiber": 30,
                "potassium": 600,
                "sodium": 2000,
            }
        }
