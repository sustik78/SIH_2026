"""
PRAMAN AI - Authentication Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..database import get_db
from ..models import User, AuditLog
from ..auth import verify_password, create_access_token, get_current_user, hash_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    badge_number: Optional[str] = None
    department: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid enforcement credentials (username or password)."
        )

    # Log audit entry
    audit = AuditLog(
        user_id=user.id,
        username=user.username,
        action="USER_LOGIN",
        entity_type="USER",
        entity_id=str(user.id),
        details=f"User {user.username} ({user.role}) logged in successfully."
    )
    db.add(audit)
    db.commit()

    token = create_access_token({"sub": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "badge_number": user.badge_number,
            "department": user.department
        }
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "badge_number": current_user.badge_number,
        "department": current_user.department
    }

@router.get("/users", response_model=List[UserResponse])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "badge_number": u.badge_number,
            "department": u.department
        }
        for u in users
    ]
