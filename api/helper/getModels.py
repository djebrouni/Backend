from api.models import Patient, Doctor, Nurse, LabTechnician, Radiologist, administratifStaff
from api.const.ROLES import ROLES

def getModel(role):
    # Normalize role input
    try:
        print(role)
        role = role.strip().lower()  # Trim spaces and lowercase
    except: return None
    
    # Match roles with normalized values
    if role == ROLES.Patient.value:
        return Patient
    elif role == ROLES.Doctor.value:
        return Doctor
    elif role == ROLES.Nurse.value:
        return Nurse
    elif role == ROLES.LabTechnician.value:
        return LabTechnician
    elif role == ROLES.Radiologist.value:
        return Radiologist
    elif role == ROLES.administratifStaff.value:
        return administratifStaff
    else:
        return None