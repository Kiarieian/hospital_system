<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Users
from app.database import get_db
from passlib.context import CryptContext

router = APIRouter(prefix="/staff", tags=["Staff"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def staff_login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful", "username": user.username, "role": user.role}

    #create token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})  
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 🧑‍⚕️ Create a doctor user
@router.post("/create_doctor")
def create_doctor(username: str, password: str, email: str, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(Users).filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Hash password
    hashed_password = pwd_context.hash(password)

    # Create doctor user
    new_doctor = Users(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="doctor",
        is_active=True
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {"message": "Doctor created successfully", "doctor_username": new_doctor.username}


# 👩‍⚕️ Create a nurse user
@router.post("/create_nurse")
def create_nurse(username: str, password: str, email: str, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = pwd_context.hash(password)

    new_nurse = Users(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="nurse",
        is_active=True
    )

    db.add(new_nurse)
    db.commit()
    db.refresh(new_nurse)

    return {"message": "Nurse created successfully", "nurse_username": new_nurse.username}


# 🧍 Receptionist user
@router.post("/create_receptionist")
def create_receptionist(username: str, password: str, email: str, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = pwd_context.hash(password)

    new_receptionist = Users(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="receptionist",
        is_active=True
    )

    db.add(new_receptionist)
    db.commit()
    db.refresh(new_receptionist)

    return {"message": "Receptionist created successfully", "receptionist_username": new_receptionist.username}
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Users
from app.database import get_db
from passlib.context import CryptContext

router = APIRouter(prefix="/staff", tags=["Staff"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def staff_login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful", "username": user.username, "role": user.role}

    #create token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})  
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 🧑‍⚕️ Create a doctor user
@router.post("/create_doctor")
def create_doctor(username: str, password: str, email: str, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(Users).filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Hash password
    hashed_password = pwd_context.hash(password)

    # Create doctor user
    new_doctor = Users(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="doctor",
        is_active=True
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {"message": "Doctor created successfully", "doctor_username": new_doctor.username}


# 👩‍⚕️ Create a nurse user
@router.post("/create_nurse")
def create_nurse(username: str, password: str, email: str, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = pwd_context.hash(password)

    new_nurse = Users(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="nurse",
        is_active=True
    )

    db.add(new_nurse)
    db.commit()
    db.refresh(new_nurse)

    return {"message": "Nurse created successfully", "nurse_username": new_nurse.username}


# 🧍 Receptionist user
@router.post("/create_receptionist")
def create_receptionist(username: str, password: str, email: str, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        (Users.username == username) | (Users.email == email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = pwd_context.hash(password)

    new_receptionist = Users(
        username=username,
        email=email,
        password_hash=hashed_password,
        role="receptionist",
        is_active=True
    )

    db.add(new_receptionist)
    db.commit()
    db.refresh(new_receptionist)

    return {"message": "Receptionist created successfully", "receptionist_username": new_receptionist.username}
>>>>>>> aaafd8a56da777b197aae0be4a0ad9b36eeac6a1
