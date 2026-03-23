from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.database import User, db_dependency
from app.utils.auth import bcrypt_context

router = APIRouter(prefix='/auth',tags=['auth'])

@router.get('/')
async def authenticate_user(request: Annotated[dict, Depends(OAuth2PasswordRequestForm)], db: db_dependency):
    email = request.get("user_email")
    password = request.get("user_password")

    if not email or not password or email is None or password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    
    user_details = db.query(User).filter(User.email == email).first()

    if user_details is None:
        return {"status": "error", "message": "Email address or password is wrong. Please try again letter!"}
    
    if True is not bcrypt_context.verify(user_details.)