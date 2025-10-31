from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal
from app import auth
from app.routes import admissions, auth_routes, staff
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  
from fastapi import Request

app = FastAPI()

app.include_router(auth.router)
app.include_router(staff.router)
app.include_router(admissions.router)
app.include_router(auth_routes.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")  


@app.get("/")
def root():
    return {"message": "Hospital Management System API"}

# create tables if not present
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/beds/")
def add_bed(ward_type: str, bed_number: str, db: Session = Depends(get_db)):
    # create a bed record
    bed = models.Bed(ward_type=ward_type, bed_number=bed_number, is_occupied=False)
    db.add(bed)
    db.commit()
    db.refresh(bed)
    return {"message": "Bed added", "id": bed.id, "bed_number": bed.bed_number}

@app.post("/patients/", response_model=schemas.PatientResponse)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    # 1) Create patient record
    patient = models.Patient(
        full_name=payload.full_name,
        gender=payload.gender,
        ward_type=payload.ward_type,
        contact=payload.contact,
        address=payload.address,
        is_admitted=payload.is_admitted
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    # 2) If admission requested, try to find a free bed in that ward_type
    if payload.is_admitted:
        if not payload.ward_type:
            raise HTTPException(status_code=400, detail="ward_type required to admit patient")

        # Free bed and matching
        free_bed = (
            db.query(models.Bed)
            .filter(models.Bed.ward_type == payload.ward_type, models.Bed.is_occupied == False)
            .first()
        )

        if not free_bed:
            # no free bed 
            raise HTTPException(status_code=400, detail=f"No free beds available in ward '{payload.ward_type}'")

        # mark bed occupied and create admission record
        free_bed.is_occupied = True
        patient.is_admitted = True
        patient_bed_number = free_bed.bed_number

        # link ward:
        ward = db.query(models.Ward).filter(models.Ward.ward_name == payload.ward_type).first()
        ward_id = ward.id if ward else None
        if ward:
            ward.occupied_beds = (ward.occupied_beds or 0) + 1

        admission = models.Admission(
            patient_id=patient.full_name,
            ward_id=ward_id,
            bed_id=free_bed.id,
            bed_number=patient_bed_number,
            status="Admitted"
        )
        db.add(admission)
        db.commit()
        db.refresh(patient)
        db.refresh(free_bed)

    # return patient
    latest_adm = db.query(models.Admission).filter(models.Admission.patient_id == patient.full_name).order_by(models.Admission.admitted_at.desc()).first()
    bed_no = latest_adm.bed_number if latest_adm else None

    response = schemas.PatientResponse.from_orm(patient)
    response_dict = response.dict()
    response_dict["bed_number"] = bed_no
    app.include_router(auth.router)
    return response_dict


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/patients", response_class=HTMLResponse)
def patients_page(request: Request):
    return templates.TemplateResponse("patients.html", {"request": request})

