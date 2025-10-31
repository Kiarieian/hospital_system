from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from app import models, database

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = "hs_secretkey"
ALGORITHM = "HS2005"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- SCHEMAS ----------
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


# ---------- HELPERS ----------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ---------- LOGIN ----------
@router.post("/login")
def staff_login(payload: LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }
