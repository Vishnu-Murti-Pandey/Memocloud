from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from schemas.user import UserProfileResponse
from core.database import get_session
from models.user import User
from core.dependencies import get_current_user
from core.security import hash_password, verify_password, create_access_token


auth_router = APIRouter(prefix='/api/auth', tags=["Authentication"])


@auth_router.post('/register', response_model=RegisterResponse)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    name = request.name
    email = request.email
    password = request.password
    
    is_user_exist = session.exec(select(User).where(User.email == email)).first()
    if(is_user_exist):
        raise HTTPException(status_code=409, detail="User already exist.")
    
    hashed_password = hash_password(password)
    user = User(name=name, email=email, hashed_password=hashed_password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return RegisterResponse(message="User created successfully")


@auth_router.post('/login', response_model=LoginResponse)
def register(request: LoginRequest, session: Session = Depends(get_session)):
    user_email = request.email
    user_password = request.password
    
    user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist.")
    
    is_password_matched = verify_password(user_password, user.hashed_password)
    if is_password_matched == False:
        raise HTTPException(status_code=401, detail="Invalid credintials.")

    jwt_token = create_access_token(user.id, user.email, 60)
    
    return LoginResponse(message="Login succesful", access_token=jwt_token)


@auth_router.get("/user_profile", response_model= UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return UserProfileResponse(user_id=str(current_user.id), name=current_user.name, email=current_user.email)
    