from api.models import Patient, Doctor, Nurse, LabTechnician, Radiologist, administratifStaff
from api.const.ROLES import ROLES

def getModel(role):
    # Normalize role input
    role = role.strip().lower()  # Trim spaces and lowercase

    # Match roles with normalized values
    if role == ROLES.Patient.value.lower():
        return Patient
    elif role == ROLES.Doctor.value.lower():
        return Doctor
    elif role == ROLES.Nurse.value.lower():
        return Nurse
    elif role == ROLES.LabTechnician.value.lower():
        return LabTechnician
    elif role == ROLES.Radiologist.value.lower():
        return Radiologist
    elif role == ROLES.administratifStaff.value.lower():
        return administratifStaff
    else:
        raise ValueError(f"User role '{role}' not recognized.")
