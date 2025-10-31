<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from .database import Base
import enum

# ENUM FOR USER ROLES

class RoleEnum(enum.Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"
    receptionist = "receptionist"


# USERS TABLE

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False, default="nurse")  # or Enum(RoleEnum)
    

    # Relationships
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    nurse_profile = relationship("Nurse", back_populates="user", uselist=False)
    receptionist_profile = relationship("Reception", back_populates="user", uselist=False)
    


# DOCTOR TABLE

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    specialty = Column(String(100))
    status = Column(String(50), default="Active")
    contact = Column(String(20), unique=True)
    ward_id = Column(Integer, ForeignKey("wards.id"))

    # Relationships
    user = relationship("Users", back_populates="doctor_profile")
    ward = relationship("Ward", back_populates="doctors")
    admissions = relationship("Admission", back_populates="doctor")


# NURSE TABLE

class Nurse(Base):
    __tablename__ = "nurses"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    contact = Column(String(20), unique=True)
    ward_id = Column(Integer, ForeignKey("wards.id"))

    # Relationships
    user = relationship("Users", back_populates="nurse_profile")
    ward = relationship("Ward", back_populates="nurses")
    admissions = relationship("Admission", back_populates="nurse")


# ------------------------------
# RECEPTION TABLE
# ------------------------------
class Reception(Base):
    __tablename__ = "receptions"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    desk_number = Column(String(20))

    # Relationships
    user = relationship("Users", back_populates="receptionist_profile")


# WARD TABLE
class Ward(Base):
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True)
    ward_name = Column(String(100), unique=True, nullable=False)
    total_beds = Column(Integer, nullable=False)
    occupied_beds = Column(Integer, default=0)

    # Relationships
    doctors = relationship("Doctor", back_populates="ward")
    nurses = relationship("Nurse", back_populates="ward")
    admissions = relationship("Admission", back_populates="ward")
    beds = relationship("Bed", back_populates="ward")
    equipment = relationship("Equipment", back_populates="ward")


# PATIENT TABLE

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    contact = Column(String(20), unique=True)
    address = Column(String(200))
    date_of_birth = Column(Date)
    is_admitted = Column(Boolean, default=False)
    ward_type = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    admissions = relationship("Admission", back_populates="patient")

# ADMISSION TABLE

class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    nurse_id = Column(Integer, ForeignKey("nurses.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    bed_id = Column(Integer, ForeignKey("beds.id"))
    status = Column(String(50), default="Admitted")
    admitted_at = Column(DateTime, server_default=func.now())
    discharged_at = Column(DateTime, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="admissions")
    doctor = relationship("Doctor", back_populates="admissions")
    nurse = relationship("Nurse", back_populates="admissions")
    ward = relationship("Ward", back_populates="admissions")
    bed = relationship("Bed", back_populates="admission")


# BED TABLE

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    bed_number = Column(String(20), nullable=False)
    ward_type = Column(String(100), nullable=False)
    ward_id = Column(Integer, ForeignKey("wards.id"))
    is_occupied = Column(Boolean, default=False)

    ward = relationship("Ward", back_populates="beds")
    admission = relationship("Admission", back_populates="bed", uselist=False)


# EQUIPMENT TABLE
class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = (UniqueConstraint('equipment_name', 'ward_id', name='uix_equipment_ward'),)

    id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    ward_id = Column(Integer, ForeignKey("wards.id"))
    condition = Column(String(50), default="Good")

    ward = relationship("Ward", back_populates="equipment")
=======
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from .database import Base
import enum

# ENUM FOR USER ROLES

class RoleEnum(enum.Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"
    receptionist = "receptionist"


# USERS TABLE

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False, default="nurse")  # or Enum(RoleEnum)
    

    # Relationships
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    nurse_profile = relationship("Nurse", back_populates="user", uselist=False)
    receptionist_profile = relationship("Reception", back_populates="user", uselist=False)
    


# DOCTOR TABLE

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    specialty = Column(String(100))
    status = Column(String(50), default="Active")
    contact = Column(String(20), unique=True)
    ward_id = Column(Integer, ForeignKey("wards.id"))

    # Relationships
    user = relationship("Users", back_populates="doctor_profile")
    ward = relationship("Ward", back_populates="doctors")
    admissions = relationship("Admission", back_populates="doctor")


# NURSE TABLE

class Nurse(Base):
    __tablename__ = "nurses"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    contact = Column(String(20), unique=True)
    ward_id = Column(Integer, ForeignKey("wards.id"))

    # Relationships
    user = relationship("Users", back_populates="nurse_profile")
    ward = relationship("Ward", back_populates="nurses")
    admissions = relationship("Admission", back_populates="nurse")


# ------------------------------
# RECEPTION TABLE
# ------------------------------
class Reception(Base):
    __tablename__ = "receptions"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    desk_number = Column(String(20))

    # Relationships
    user = relationship("Users", back_populates="receptionist_profile")


# WARD TABLE
class Ward(Base):
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True)
    ward_name = Column(String(100), unique=True, nullable=False)
    total_beds = Column(Integer, nullable=False)
    occupied_beds = Column(Integer, default=0)

    # Relationships
    doctors = relationship("Doctor", back_populates="ward")
    nurses = relationship("Nurse", back_populates="ward")
    admissions = relationship("Admission", back_populates="ward")
    beds = relationship("Bed", back_populates="ward")
    equipment = relationship("Equipment", back_populates="ward")


# PATIENT TABLE

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    contact = Column(String(20), unique=True)
    address = Column(String(200))
    date_of_birth = Column(Date)
    is_admitted = Column(Boolean, default=False)
    ward_type = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    admissions = relationship("Admission", back_populates="patient")

# ADMISSION TABLE

class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    nurse_id = Column(Integer, ForeignKey("nurses.id"))
    ward_id = Column(Integer, ForeignKey("wards.id"))
    bed_id = Column(Integer, ForeignKey("beds.id"))
    status = Column(String(50), default="Admitted")
    admitted_at = Column(DateTime, server_default=func.now())
    discharged_at = Column(DateTime, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="admissions")
    doctor = relationship("Doctor", back_populates="admissions")
    nurse = relationship("Nurse", back_populates="admissions")
    ward = relationship("Ward", back_populates="admissions")
    bed = relationship("Bed", back_populates="admission")


# BED TABLE

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    bed_number = Column(String(20), nullable=False)
    ward_type = Column(String(100), nullable=False)
    ward_id = Column(Integer, ForeignKey("wards.id"))
    is_occupied = Column(Boolean, default=False)

    ward = relationship("Ward", back_populates="beds")
    admission = relationship("Admission", back_populates="bed", uselist=False)


# EQUIPMENT TABLE
class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = (UniqueConstraint('equipment_name', 'ward_id', name='uix_equipment_ward'),)

    id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    ward_id = Column(Integer, ForeignKey("wards.id"))
    condition = Column(String(50), default="Good")

    ward = relationship("Ward", back_populates="equipment")
>>>>>>> aaafd8a56da777b197aae0be4a0ad9b36eeac6a1
