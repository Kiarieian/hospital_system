<<<<<<< HEAD
# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatientBase(BaseModel):
    full_name: str
    gender: Optional[str] = None
    ward_type: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    is_admitted: Optional[bool] = False

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    bed_number: Optional[str] = None

    class Config:
        orm_mode = True
=======
# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatientBase(BaseModel):
    full_name: str
    gender: Optional[str] = None
    ward_type: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    is_admitted: Optional[bool] = False

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    bed_number: Optional[str] = None

    class Config:
        orm_mode = True
>>>>>>> aaafd8a56da777b197aae0be4a0ad9b36eeac6a1
