from fastapi import APIRouter, Body, HTTPException, Response, status

from app.models.database import User, db_dependency
from app.models.schemas import UserSchema
from app.utils.auth import bcrypt_context, generate_token

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post('/')
async def authenticate_user(db: db_dependency, response: Response, request: dict = Body(...)):
    email = request.get("username")
    password = request.get("password")

    if not email or not password or email is None or password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    user_details = db.query(User).filter(User.email == email).first()

    if user_details is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email address or password is wrong.")
    elif not bcrypt_context.verify(password, user_details.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email address or password is wrong.")
    else:
        token = generate_token(email)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="strict",
            path="/",
            max_age=3600,
        )
        return {"status": "success", "message": "Login successful!"}
    
@router.post('/register')
async def register_user(request: UserSchema, db: db_dependency):
    is_exist_user = db.query(User).filter(User.email == request.email).one_or_none()

    if is_exist_user is not None:
        raise HTTPException(status_code=409, detail="User already exists!")
    
    user = User(
        first_name=request.first_name,
        middle_name=request.middle_name,
        last_name=request.last_name,
        email=request.email,
        password=bcrypt_context.hash(request.password)
    )

    db.add(user)
    db.commit()
    return {"status": "success", "message": "User has been registered!"}