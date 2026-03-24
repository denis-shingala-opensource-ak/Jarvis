
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, WebSocket, status
from fastapi.responses import RedirectResponse
from app.core.exceptions import AuthRedirectException
from app.core.logging_config import logger
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.database import User, db
from app.models.schemas import JWTToken

bcrypt_context = CryptContext(['sha256_crypt', 'des_crypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/')


def auth(request: Request):
    """Auth for normal request - if not authenticated then redirect to login page."""
    try:
        token = request.cookies.get('access_token')
        if not token:
            raise AuthRedirectException()

        token_details = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        if token_details is None:
            raise AuthRedirectException()

        return JWTToken(user_id=token_details.get("user_id"), email=token_details.get("email"), exp=token_details.get("exp"))
    except (JWTError, Exception) as err:
        logger.error(f"JWT Error: {err}")
        raise AuthRedirectException()

user_dependency = Annotated[JWTToken, Depends(auth)]

def ws_auth(websocket: WebSocket):
    """Auth for WebSocket — returns JWTToken or None."""
    try:
        token = websocket.cookies.get('access_token')
        if not token:
            return None

        token_details = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if token_details is None:
            return None

        return JWTToken(user_id=token_details.get("user_id"), email=token_details.get("email"), exp=token_details.get("exp"))
    except (JWTError, Exception) as err:
        logger.error(f"WebSocket JWT Error: {err}")
        return None

ws_user_dependency = Annotated[JWTToken, Depends(ws_auth)]

def generate_token(email: str):
    """ Create the JWT token for the authenticate the user """
    try:
        user = db.query(User).filter(User.email == email).first()

        if user is not None:
            expire_time = datetime.now(timezone.utc) + timedelta(minutes=1)
            token = jwt.encode({
                "user_id": user.id,
                "email": email,
                "exp": expire_time.timestamp()
            }, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

            return token
        else:
            raise JWTError({'message': 'User not exists'})
    except JWTError as e:
        raise Exception({'status': 'error', 'message': e})
