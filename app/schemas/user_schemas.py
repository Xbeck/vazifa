"""Define Schemas used by the User routes."""


from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import RoleType
from app.schemas.examples import ExampleUser


class UserBase(BaseModel):
    """Base for the User Schema."""

    model_config = ConfigDict(from_attributes=True)

    email: str = Field(examples=[ExampleUser.email])


class UserRegisterRequest(UserBase):
    """Request schema for the Register Route."""

    password: str = Field(examples=[ExampleUser.password])
    first_name: str = Field(examples=[ExampleUser.first_name])
    last_name: str = Field(examples=[ExampleUser.last_name])


class UserLoginRequest(UserBase):
    """Request schema for the Login Route."""

    password: str = Field(examples=[ExampleUser.password])


class UserEditRequest(UserBase):
    """Request schema for Editing a User.

    For now just inherit everything from the UserRegisterRequest
    """

    model_config = ConfigDict(from_attributes=True)

    email: str = Field(examples=[ExampleUser.email])
    password: str = Field(examples=[ExampleUser.password])
    first_name: str = Field(examples=[ExampleUser.first_name])
    last_name: str = Field(examples=[ExampleUser.last_name])


class UserChangePasswordRequest(BaseModel):
    """Request Schema for changing a user's password."""

    password: str = Field(examples=[ExampleUser.password])




"""Define Response schemas specific to the Users."""

class UserResponse(UserBase):
    """Response Schema for a User."""

    id: int = Field(ExampleUser.id)
    first_name: str = Field(examples=[ExampleUser.first_name])
    last_name: str = Field(examples=[ExampleUser.last_name])
    role: RoleType = Field(examples=[ExampleUser.role])
    banned: bool = Field(examples=[ExampleUser.banned])
    verified: bool = Field(examples=[ExampleUser.verified])


class MyUserResponse(UserBase):
    """Response for non-admin getting their own User data."""

    first_name: str = Field(examples=[ExampleUser.first_name])
    last_name: str = Field(examples=[ExampleUser.last_name])