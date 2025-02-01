"""Define routes for Authentication."""

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_database
from app.managers.auth import AuthManager
from app.managers.user_manager import UserManager
from app.schemas.auth import TokenRefreshRequest, TokenRefreshResponse, TokenResponse
from app.schemas.user_schemas import UserLoginRequest, UserRegisterRequest

router = APIRouter(tags=["Authentication"])


@router.post("/register/", status_code=status.HTTP_201_CREATED, name="register_a_new_user", response_model=TokenResponse)
async def register(user_data: UserRegisterRequest, session: AsyncSession = Depends(get_database)) -> dict[str, str]:
    """Register a new User and return a JWT token plus a Refresh Token.

    The JWT token should be sent as a Bearer token for each access to a
    protected route. It will expire after 120 minutes.

    When the JWT expires, the Refresh Token can be sent using the '/refresh'
    endpoint to return a new JWT Token. The Refresh token will last 30 days, and
    cannot be refreshed.
    """
    token, refresh = await UserManager.register(user_data.model_dump(), session=session)
    return {"token": token, "refresh": refresh}


@router.post("/login/", name="login_an_existing_user", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user_data: UserLoginRequest, session: AsyncSession = Depends(get_database)) -> dict[str, str]:
    """Login an existing User and return a JWT token plus a Refresh Token.

    The JWT token should be sent as a Bearer token for each access to a
    protected route. It will expire after 120 minutes.

    When the JWT expires, the Refresh Token can be sent using the '/refresh'
    endpoint to return a new JWT Token. The Refresh token will last 30 days, and
    cannot be refreshed.
    """
    token, refresh = await UserManager.login(user_data.model_dump(), session)
    return {"token": token, "refresh": refresh}


@router.post("/refresh/", name="refresh_an_expired_token", response_model=TokenRefreshResponse)
async def generate_refresh_token(refresh_token: TokenRefreshRequest, session: AsyncSession = Depends(get_database)) -> dict[str, str]:
    """Return a new JWT, given a valid Refresh token.

    The Refresh token will not be updated at this time, it will still expire 30
    days after original issue. At that time the User will need to login again.
    """
    token = await AuthManager.refresh(refresh_token, session)
    return {"token": token}
