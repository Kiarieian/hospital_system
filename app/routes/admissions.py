<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app import models, database
from app.routes.dependancies import require_role

router = APIRouter(prefix="/admissions", tags=["Admissions"])


# ---------- SCHEMAS ----------
class AdmissionRequest(BaseModel):
    patient_id: int
    doctor_id: int
    ward_type: str
    bed_id: int


class PatientCreate(BaseModel):
    full_name: str
    gender: str
    contact: str | None = None
    address: str | None = None
    date_of_birth: datetime | None = None
    is_admitted: bool = False
    ward_type: str | None = None


# ---------- REGISTER NEW PATIENT ----------
@router.post("/patients", status_code=201,dependencies=[Depends(require_role(["admin","receptionist","nurse"]))] )
def register_patient(payload: PatientCreate, db: Session = Depends(database.get_db)):
    existing_patient = db.query(models.Patient).filter(
        models.Patient.full_name == payload.full_name,
        models.Patient.date_of_birth == payload.date_of_birth
    ).first()

    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient already registered")

    new_patient = models.Patient(
        full_name=payload.full_name,
        gender=payload.gender,
        contact=payload.contact,
        address=payload.address,
        date_of_birth=payload.date_of_birth,
        is_admitted=payload.is_admitted,
        ward_type=payload.ward_type
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "Patient registered successfully", "patient_id": new_patient.id}


# ---------- ADMIT PATIENT ----------
@router.post("/admit", status_code=201,dependencies=[Depends(require_role(["admin","doctor","nurse" ]))])
def admit_patient(payload: AdmissionRequest, db: Session = Depends(database.get_db), current_user: models.Users = Depends(require_role(["admin","doctor","nurse"]))):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if patient.is_admitted:
        raise HTTPException(status_code=400, detail="Patient is already admitted")

    bed = db.query(models.Bed).filter(
        models.Bed.id == payload.bed_id,
        models.Bed.ward_type == payload.ward_type,
        models.Bed.is_occupied == False
    ).first()

    if not bed:
        raise HTTPException(status_code=404, detail=f"No available bed found for ward type: {payload.ward_type}")

    admission = models.Admission(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        ward_id=bed.ward_id,
        bed_id=payload.bed_id,
        admitted_at=datetime.utcnow(),
        status="Admitted"
    )

    bed.is_occupied = True
    patient.is_admitted = True

    db.add(admission)
    db.commit()
    db.refresh(admission)

    return {"message": "Patient admitted successfully", "admission_id": admission.id}


# ---------- DISCHARGE PATIENT ----------
@router.put("/discharge/{patient_id}",dependencies=[Depends(require_role(["admin","doctor","nurse"]))]  )
def discharge_patient(patient_id: int, db: Session = Depends(database.get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not patient.is_admitted:
        raise HTTPException(status_code=400, detail="Patient is not currently admitted")

    admission = db.query(models.Admission).filter(
        models.Admission.patient_id == patient_id,
        models.Admission.status == "Admitted"
    ).first()

    if not admission:
        raise HTTPException(status_code=404, detail="Active admission record not found for this patient")

    bed = db.query(models.Bed).filter(models.Bed.id == admission.bed_id).first()
    if bed:
        bed.is_occupied = False

    admission.status = "Discharged"
    admission.discharged_at = datetime.utcnow()
    patient.is_admitted = False

    db.commit()
    db.refresh(admission)

    return {"message": "Patient discharged successfully", "admission_id": admission.id}


# ---------- GET ALL PATIENTS ----------
@router.get("/patients", status_code=200)
def list_patients(db: Session = Depends(database.get_db)):
    patients = db.query(models.Patient).all()
    return patients


# ---------- GET ALL ADMISSIONS ----------
@router.get("/admissions", status_code=200)
def list_admissions(db: Session = Depends(database.get_db)):
    admissions = db.query(models.Admission).all()
    return admissions


# ---------- GET SINGLE ADMISSION ----------
@router.get("/admissions/{patient_id}", status_code=200)
def get_admission(patient_id: int, db: Session = Depends(database.get_db)):
    admission = db.query(models.Admission).filter(models.Admission.patient_id == patient_id).first()
    if not admission:
        raise HTTPException(status_code=404, detail="No admission found for this patient")
    return admission

=======
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app import models, database
from app.routes.dependancies import require_role

router = APIRouter(prefix="/admissions", tags=["Admissions"])


# ---------- SCHEMAS ----------
class AdmissionRequest(BaseModel):
    patient_id: int
    doctor_id: int
    ward_type: str
    bed_id: int


class PatientCreate(BaseModel):
    full_name: str
    gender: str
    contact: str | None = None
    address: str | None = None
    date_of_birth: datetime | None = None
    is_admitted: bool = False
    ward_type: str | None = None


# ---------- REGISTER NEW PATIENT ----------
@router.post("/patients", status_code=201,dependencies=[Depends(require_role(["admin","receptionist","nurse"]))] )
def register_patient(payload: PatientCreate, db: Session = Depends(database.get_db)):
    existing_patient = db.query(models.Patient).filter(
        models.Patient.full_name == payload.full_name,
        models.Patient.date_of_birth == payload.date_of_birth
    ).first()

    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient already registered")

    new_patient = models.Patient(
        full_name=payload.full_name,
        gender=payload.gender,
        contact=payload.contact,
        address=payload.address,
        date_of_birth=payload.date_of_birth,
        is_admitted=payload.is_admitted,
        ward_type=payload.ward_type
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "Patient registered successfully", "patient_id": new_patient.id}


# ---------- ADMIT PATIENT ----------
@router.post("/admit", status_code=201,dependencies=[Depends(require_role(["admin","doctor","nurse" ]))])
def admit_patient(payload: AdmissionRequest, db: Session = Depends(database.get_db), current_user: models.Users = Depends(require_role(["admin","doctor","nurse"]))):
    patient = db.query(models.Patient).filter(models.Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if patient.is_admitted:
        raise HTTPException(status_code=400, detail="Patient is already admitted")

    bed = db.query(models.Bed).filter(
        models.Bed.id == payload.bed_id,
        models.Bed.ward_type == payload.ward_type,
        models.Bed.is_occupied == False
    ).first()

    if not bed:
        raise HTTPException(status_code=404, detail=f"No available bed found for ward type: {payload.ward_type}")

    admission = models.Admission(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        ward_id=bed.ward_id,
        bed_id=payload.bed_id,
        admitted_at=datetime.utcnow(),
        status="Admitted"
    )

    bed.is_occupied = True
    patient.is_admitted = True

    db.add(admission)
    db.commit()
    db.refresh(admission)

    return {"message": "Patient admitted successfully", "admission_id": admission.id}


# ---------- DISCHARGE PATIENT ----------
@router.put("/discharge/{patient_id}",dependencies=[Depends(require_role(["admin","doctor","nurse"]))]  )
def discharge_patient(patient_id: int, db: Session = Depends(database.get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not patient.is_admitted:
        raise HTTPException(status_code=400, detail="Patient is not currently admitted")

    admission = db.query(models.Admission).filter(
        models.Admission.patient_id == patient_id,
        models.Admission.status == "Admitted"
    ).first()

    if not admission:
        raise HTTPException(status_code=404, detail="Active admission record not found for this patient")

    bed = db.query(models.Bed).filter(models.Bed.id == admission.bed_id).first()
    if bed:
        bed.is_occupied = False

    admission.status = "Discharged"
    admission.discharged_at = datetime.utcnow()
    patient.is_admitted = False

    db.commit()
    db.refresh(admission)

    return {"message": "Patient discharged successfully", "admission_id": admission.id}


# ---------- GET ALL PATIENTS ----------
@router.get("/patients", status_code=200)
def list_patients(db: Session = Depends(database.get_db)):
    patients = db.query(models.Patient).all()
    return patients


# ---------- GET ALL ADMISSIONS ----------
@router.get("/admissions", status_code=200)
def list_admissions(db: Session = Depends(database.get_db)):
    admissions = db.query(models.Admission).all()
    return admissions


# ---------- GET SINGLE ADMISSION ----------
@router.get("/admissions/{patient_id}", status_code=200)
def get_admission(patient_id: int, db: Session = Depends(database.get_db)):
    admission = db.query(models.Admission).filter(models.Admission.patient_id == patient_id).first()
    if not admission:
        raise HTTPException(status_code=404, detail="No admission found for this patient")
    return admission

>>>>>>> aaafd8a56da777b197aae0be4a0ad9b36eeac6a1
