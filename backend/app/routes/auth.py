from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import timedelta
from typing import Any

from ..models.user import UserCreate, UserLogin, Token, User
from ..controllers.user_controller import UserController
from ..core.security import create_access_token, verify_password
from ..core.config import settings
from ..utils.auth import get_current_active_user

router = APIRouter()
security = HTTPBearer()

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate) -> Any:
    """Register a new parent user."""
    user_controller = UserController()
    
    try:
        # Create user
        user = await user_controller.create_user(user_data)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin) -> Any:
    """Authenticate user and return access token."""
    user_controller = UserController()
    
    # Authenticate user
    user = await user_controller.authenticate_user(
        email=credentials.email,
        password=credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user
    )

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_active_user)) -> Any:
    """Refresh access token."""
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email, "user_id": current_user.id},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=current_user
    )

@router.get("/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_active_user)) -> Any:
    """Get current user profile."""
    return current_user

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)) -> Any:
    """Logout user (client-side token removal)."""
    return {"message": "Successfully logged out"}

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_active_user)) -> Any:
    """Verify if token is valid."""
    return {"valid": True, "user": current_user}
