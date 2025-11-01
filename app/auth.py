
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, database
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str

@router.post("/register")
def register_user(payload: RegisterRequest, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existing_user = db.query(models.Users).filter(models.Users.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = hash_password(payload.password)

    # Create new user record
    new_user = models.Users(
        username=payload.username,
        email=payload.email,
        password_hash=hashed_password,
        role=payload.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "username": new_user.username}

# 1️⃣ JWT Configuration    
SECRET_KEY = "User"  #  env variable later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 2️⃣ Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 3️⃣ Password utilities
def hash_password(password: str):
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 4️⃣ Token generation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 5️⃣ Authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

# 6️⃣ Get current logged-in user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if user is None:
        raise credentials_exception
    return user

