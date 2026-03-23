
from typing import Annotated

from fastapi import Depends, HTTPException, Request, responses, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext

bcrypt_context = CryptContext(['sha256_crypt', 'des_crypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='')

def auth(token: Request):
    try:
        if token is None:
            responses.RedirectResponse("/login")
        
        token_details = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        if token_details is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Jwt token is expired!")
        
        return {"user_id": token_details.get("user_id"), "email": token_details.get("user_email")}
    except Exception as e:
        pass

user_dependency = Annotated[dict, Depends(auth)]