from enum import Enum
from django.db import models
from django.core.validators import MinValueValidator

#enum class of tools  Sthetoscope or Thermometer or TensionMeter
class Tool(Enum):
    STETHOSCOPE = 'Stethoscope'
    THERMOMETER = 'Thermometer'
    TENSION_METER = 'Tension Meter'
#enum for blood types with rhesus 
class BloodType(Enum):
        A_POSITIVE = 'A+'
        A_NEGATIVE = 'A-'
        B_POSITIVE = 'B+'
        B_NEGATIVE = 'B-'
        AB_POSITIVE = 'AB+'
        AB_NEGATIVE = 'AB-'
        O_POSITIVE = 'O+'
        O_NEGATIVE = 'O-'

#EHR model 
class EHR(models.Model):
    id = models.AutoField(primary_key=True)
    
    administratifStaff = models.ForeignKey(
        'administratifStaff',  # Link to administratifStaff
        on_delete=models.CASCADE,  
        related_name='ehr_staff', 
        null=True,
        blank=True
    )


#doctor model 
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    specialization = models.CharField(max_length=45) 
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)

    ehr = models.ManyToManyField(
        EHR,  # Reference to the EHR model
        related_name='doctors',  # Allows access to all doctors associated with a specific EHR
        blank=True  
    )




#Hospital model 
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=45)

# Patient model
class Patient(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    NSS = models.PositiveIntegerField(unique=True)  # National Social Security number, for example
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    dateOfBirth = models.DateField()
    address = models.CharField(max_length=70)
    phoneNumber = models.CharField(max_length=10)
    mutual = models.CharField(max_length=45)
    contactPerson = models.CharField(max_length=45)
    bloodType = models.CharField(
        max_length=11,
        choices=[(tag.name, tag.value) for tag in BloodType],
        default=BloodType.O_POSITIVE.name  # Default blood type
    )
    gender = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, null=True, blank=True)  # nullable and blankable password field


    # Linking to the EHR model with a one-to-one relationship
    ehr = models.OneToOneField(
        EHR, 
        on_delete=models.CASCADE, 
        related_name='patient', 
        null=True, 
        blank=True  # Optional: if not all patients have an EHR initially
    )

    hospital = models.ForeignKey(
        Hospital,  # Link to the Hospital model
        on_delete=models.CASCADE,  # If the hospital is deleted, delete all associated patients
        related_name='patients',  # This allows access to all patients belonging to a specific hospital
        null=True,
        blank=True  # Optional: If not all patients are associated with a hospital
    )


# admin Model 
class administratifStaff(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    email = models.CharField(max_length=70)
    password=models.CharField(max_length=200)
    #link this model with the EHR model one to many relationship
    


class approvedMedications(models.Model):
    id = models.AutoField(primary_key=True)
    number=models.IntegerField()

#LabTechnician model 
class LabTechnician(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    specialization = models.CharField(max_length=45)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)


#Biology report model 
class BiologyReport(models.Model):
    id = models.AutoField(primary_key=True)
    bloodSugarLevel = models.FloatField()
    bloodPressure = models.FloatField()
    chelesterolLevel = models.FloatField()
    completeBloodCount = models.FloatField()
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,  # If the doctor is deleted, all their biology reports are deleted
        related_name='biology_reports',  # Allows you to access a doctor's biology reports
        null=False,  
        blank=True  
    )

    lab_technician = models.ForeignKey(
        LabTechnician,  # Linking to the LabTechnician model
        on_delete=models.CASCADE,  # If the LabTechnician is deleted, delete the related BiologyReports
        related_name='biology_reports',  # Allows accessing all BiologyReports for a LabTechnician
        null=False,  
        blank=True  # Optional: if not all BiologyReports have a LabTechnician linked initially
    )
#Diagnostic Model
class Diagnostic(models.Model):
    id = models.AutoField(primary_key=True)
    prescription = models.OneToOneField(
        'Prescription',  # Reference to the Prescription model
        on_delete=models.CASCADE,  # If the Diagnostic is deleted, the related Prescription is also deleted
        related_name='diagnostic',  
        null=True,  
    )

#consultation model 
class Consultation(models.Model):
    id= models.AutoField(primary_key=True)
    date = models.DateField()
    summary = models.TextField()
    chiefComplaint= models.TextField()
    done = models.BooleanField(default=False)
    
    diagnostic = models.OneToOneField(
        Diagnostic,  
        on_delete=models.CASCADE,  
        related_name='consultation',  
        null=True, 
        blank=True
    )


#Medecine model
class Medecine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

#MedicalCertificate model 
class MedicalCertificate(models.Model):
    id = models.AutoField(primary_key=True)
    requesed = models.BooleanField(default=False)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,  # If the doctor is deleted, all their medical certificates are deleted
        related_name='medical_certificates',  # Allows you to access a doctor's medical certificates
        null=True,  
        blank=True  
    )

    ehr = models.ForeignKey(
        EHR,  # Linking to the EHR model
        on_delete=models.CASCADE,  # If the EHR is deleted, delete the related MedicalCertificates
        related_name='medical_certificates',  # Allows accessing all MedicalCertificates for an EHR
        null=True,  # Allows MedicalCertificate to exist without an EHR initially
        blank=True  # Optional: if not all MedicalCertificates have an EHR linked initially
    )


#Prescription model
class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    isValid = models.BooleanField(default=False)
    date = models.DateField( auto_now_add=True) # Automatically set the field to now when the object is first created. 
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,  # If the doctor is deleted, all their prescriptions are deleted
        related_name='prescriptions',  # Allows you to access a doctor's prescriptions
        null=True,  
        blank=True 
    )

    ehr = models.ForeignKey(
        EHR,
        on_delete=models.CASCADE,  # If the EHR is deleted, delete related prescriptions
        related_name='prescriptions',  # Allows accessing prescriptions from an EHR instance
        blank=True  # Optional: If not all prescriptions have an EHR linked initially
    )


#MedicalTreatment model
class MedicalTreatment(models.Model):
    dose = models.FloatField(validators=[MinValueValidator(0)])    
    Duration = models.IntegerField(default=0)
    medicine = models.ForeignKey(
        Medecine,
        on_delete=models.CASCADE,  # Cascade delete: if a Medicine is deleted, delete related MedicalTreatments
        related_name='medical_treatments',  # Allows accessing the treatments related to a specific medicine
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,  # If the Prescription is deleted, delete related MedicalTreatments
        related_name='medical_treatments',  # Allows accessing all MedicalTreatments for a Prescription
        null=True,  # Allows MedicalTreatment to exist without a Prescription initially
        blank=True  # Optional: If not all MedicalTreatments have a Prescription linked initially
    )


#Nurse model 
class Nurse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)
    
    ehr = models.ManyToManyField(
        EHR,
        related_name='nurses',  # Allows accessing the nurses related to an EHR
        blank=True  
    )

#Observation model
class Observation(models.Model):
    id= models.AutoField(primary_key=True)
    description = models.TextField()


#Radiologist model
class Radiologist(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    specialization = models.CharField(max_length=45)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)

#RadiologyReport model
class RadiologyReport(models.Model):
    id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=45)
    imageData = models.BinaryField()
    date = models.DateField()
    description = models.TextField()
    
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,  # If the doctor is deleted, all their radiology reports are deleted
        related_name='radiology_reports',  # Allows you to access a doctor's radiology reports
        null=False,  # Optional: A RadiologyReport can exist without a Doctor initially
        blank=True  # Optional: Allows the field to be left blank in forms
    )

    radiologist = models.ForeignKey(
        Radiologist,  # Linking to the Radiologist model
        on_delete=models.CASCADE,  # If the Radiologist is deleted, delete the related RadiologyReports
        related_name='radiology_reports',  # Allows accessing all RadiologyReports for a Radiologist
        null=False,  # Allows RadiologyReport to exist without a Radiologist initially
        blank=True  # Optional: if not all RadiologyReports have a Radiologist linked initially
    )

