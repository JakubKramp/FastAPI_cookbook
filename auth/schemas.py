from pydantic import BaseModel, ConfigDict

from auth.constants import SexEnum
from auth.tests.example_data.example_users import (
    example_base_profile,
    example_profile,
    example_user_create,
    example_user_list,
)


class UserList(BaseModel):
    id: int
    email: str
    username: str

    model_config = ConfigDict(json_schema_extra={"example": example_user_list})


class UserUpdate(BaseModel):
    """
    This does not inherit from UserList intentionally, because email and username are nullable here.
    """

    email: str | None = None
    username: str | None = None
    password: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": example_user_create})


class UserCreate(BaseModel):
    password: str
    email: str
    username: str

    model_config = ConfigDict(json_schema_extra={"example": example_user_create})


class UpdateProfile(BaseModel):
    sex: SexEnum | None = None
    activity_factor: str | None = None
    age: int | None = None
    height: int | None = None
    weight: int | None = None
    smoking: bool | None = None


class BaseProfile(BaseModel):
    sex: SexEnum
    activity_factor: str | None
    age: int
    height: int
    weight: int
    smoking: bool

    model_config = ConfigDict(json_schema_extra={"example": example_base_profile})


class DietaryReferenceIntakes(BaseModel):
    calories: float | None
    carbohydrates: float | None
    fat: float | None
    protein: float | None
    fiber: float | None
    potassium: float | None
    sodium: float | None


class ProfileDetail(BaseProfile):
    calories: float | None = None
    carbohydrates: float | None = None
    fat: float | None = None
    protein: float | None = None
    fiber: float | None = None
    potassium: float | None = None
    sodium: float | None = None

    model_config = ConfigDict(json_schema_extra={"example": example_profile})


class UserDetail(UserList):
    id: int
    profile: ProfileDetail | None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
