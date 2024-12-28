from models import Patient, Doctor, Nurse, LabTechnician, Radiologist, administratifStaff
from const.ROLES import ROLES

def getModel(role):
    if role == ROLES.Patient.value:
        return Patient
    elif role == ROLES.Medecin.value:
        return Doctor
    elif role == ROLES.Infirmier.value:
        return Nurse
    elif role == ROLES.Laboratin.value:
        return LabTechnician
    elif role == ROLES.Radiologue.value:
        return Radiologist
    elif role == ROLES.Personnel.value:
        return administratifStaff
    # elif role == ROLES.Admin.value:
    #     return Admin  # Or return any specific model for Admin, if you have it.
    else:
        return None