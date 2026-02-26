from pydantic import BaseModel, ConfigDict

from auth.constants import SexEnum
from auth.tests.test_data.users import create_user, update_user, profile, dri_data, profile_detail, user_detail


class UserList(BaseModel):
    """
    Minimal schema for user.
    """
    email: str
    username: str

    model_config = ConfigDict(json_schema_extra={"example": create_user})


class UserUpdate(BaseModel):
    """
    This does not inherit from UserList intentionally, because email and username are nullable here.
    """

    email: str | None = None
    username: str | None = None
    password: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": update_user})


class UserCreate(UserList):
    """
    Schema for creating user
    """
    password: str | None

    model_config = ConfigDict(json_schema_extra={"example": update_user})

class UpdateProfile(BaseModel):
    sex: SexEnum | None = None
    activity_factor: str | None = None
    age: int | None = None
    height: int | None = None
    weight: int | None = None
    smoking: bool | None = None

    model_config = ConfigDict(json_schema_extra={"example": profile})


class BaseProfile(BaseModel):
    sex: SexEnum
    activity_factor: str | None
    age: int
    height: int
    weight: int
    smoking: bool

    model_config = ConfigDict(json_schema_extra={"example": profile})


class DietaryReferenceIntakes(BaseModel):
    calories: float | None
    carbohydrates: float | None
    fat: float | None
    protein: float | None
    fiber: float | None
    potassium: float | None
    sodium: float | None

    model_config = ConfigDict(json_schema_extra={"example": dri_data})


class ProfileDetail(BaseProfile):
    calories: float | None = None
    carbohydrates: float | None = None
    fat: float | None = None
    protein: float | None = None
    fiber: float | None = None
    potassium: float | None = None
    sodium: float | None = None

    model_config = ConfigDict(json_schema_extra={"example": profile_detail})


class UserDetail(UserList):
    id: int
    profile: ProfileDetail | None

    model_config = ConfigDict(json_schema_extra={"example": user_detail})


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
