from pydantic import BaseModel


class TokenRefreshRequest(BaseModel):
    """Request schema for refreshing a JWT token."""

    refresh: str


class TokenResponse(BaseModel):
    """Response Schema for Register/Login routes.

    This returns a JWT token and a Refresh token.
    """

    token: str
    refresh: str


class TokenRefreshResponse(BaseModel):
    """Return a new JWT only, after a refresh request."""

    token: str
