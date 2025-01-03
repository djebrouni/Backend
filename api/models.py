from enum import Enum
from django.db import models
from django.core.validators import MinValueValidator

from api.const.ROLES import ROLES

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




# EHR model
class EHR(models.Model):
    id = models.AutoField(primary_key=True)

    # Creator of the EHR can be either an administratif staff or a doctor
    creator = models.ForeignKey(
        'Doctor',  # Link to Doctor (optional), since Doctor can create an EHR
        on_delete=models.SET_NULL,
        related_name='created_ehrs',
        null=True, 
        blank=True  # A doctor can create an EHR
    )

    creator_staff = models.ForeignKey(
        'administratifStaff',  # Link to administratifStaff (optional)
        on_delete=models.SET_NULL,
        related_name='created_ehrs',
        null=True,
        blank=True  # Administrative staff can create an EHR
    )


# Doctor model
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    specialization = models.CharField(max_length=45)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=50, default='doctor')

    ehr = models.ManyToManyField(
        EHR,  # Reference to the EHR model
        related_name='doctors',
        blank=True
    )



#Hospital model 
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=45)

# Patient model
class Patient(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    NSS = models.CharField(max_length=255, unique=True)  # Ensure the max_length is sufficient and the value is unique
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    dateOfBirth = models.DateField(null=True)
    address = models.CharField(max_length=70, blank=True)
    phoneNumber = models.CharField(max_length=10, blank=True)
    mutual = models.CharField(max_length=45, blank=True)
    contactPerson = models.CharField(max_length=45, blank=True)
    bloodType = models.CharField(
        max_length=11,
        choices=[(tag.name, tag.value) for tag in BloodType],
        default=BloodType.O_POSITIVE.name  # Default blood type
    )
    gender = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, null=True, blank=True)  # nullable and blankable password field
    role = models.CharField(max_length=50, default=ROLES.Patient.value) 

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
    role = models.CharField(max_length=50, default='administratifStaff') 
    #link this model with the EHR model one to many relationship
    

#LabTechnician model 
class LabTechnician(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    specialization = models.CharField(max_length=45)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=50, default='LabTechnician') 



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
    medicine = models.OneToOneField(Medecine, on_delete=models.CASCADE)
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
    role = models.CharField(max_length=50, default='Nurse') 

    ehr = models.ManyToManyField(
        EHR,
        related_name='nurses',  # Allows accessing the nurses related to an EHR
        blank=True  
    )


#Radiologist model
class Radiologist(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=10)
    specialization = models.CharField(max_length=45)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=50, default='Radiologist') 


#RadiologyReport model
class RadiologyReport(models.Model):
    id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=45)
    imageData = models.ImageField(upload_to='radiology_reports/', null=True, blank=True)
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
        null=True,  # Allows RadiologyReport to exist without a Radiologist initially
        blank=True  # Optional: if not all RadiologyReports have a Radiologist linked initially
    )
   # Link to the EHR model
    ehr = models.ForeignKey(
        EHR,
        on_delete=models.CASCADE,  # If the EHR is deleted, delete the related RadiologyReport
        related_name='radiology_reports',  # Allows accessing all RadiologyReports for a specific EHR
        null=True,  # Optional: if not all RadiologyReports have an EHR linked
        blank=True  # Optional: if not all RadiologyReports have an EHR linked initially
    )

class BiologyReport(models.Model):
    id = models.AutoField(primary_key=True)
    bloodSugarLevel = models.FloatField()
    bloodPressure = models.FloatField()
    cholesterolLevel = models.FloatField()
    completeBloodCount = models.FloatField()
    doctor = models.ForeignKey(
        'Doctor',
        on_delete=models.CASCADE,
        related_name='biology_reports'
    )
    lab_technician = models.ForeignKey(
        'LabTechnician',
        on_delete=models.CASCADE,
        related_name='biology_reports',
        null=True,  # Make lab_technician optional
        blank=True  # Make lab_technician optional in forms
    )
    # Link to the EHR model
    ehr = models.ForeignKey(
        'EHR',
        on_delete=models.CASCADE,
        related_name='biology_reports',
        null=True,  # Optional: if not all BiologyReports have an EHR linked
        blank=True  # Optional: if not all BiologyReports have an EHR linked initially
    )
    date = models.DateField(auto_now_add=True)  # Set the date to the current date by default

    def __str__(self):
        return f"Biology Report {self.id} - {self.date}"

# CareProvided model
class CareProvided(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    care_actions = models.TextField()
    nurse = models.ForeignKey(
        'Nurse',
        on_delete=models.CASCADE,
        related_name='care_provided'
    )
       # Relating CareProvided to EHR
    ehr = models.ForeignKey(
        'EHR',  # Link to EHR
        on_delete=models.CASCADE,
        related_name='care_provided',  # You can access all care events for a specific EHR via this related_name
    )

# Observation model
class Observation(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    care_provided = models.ForeignKey(
        CareProvided,
        on_delete=models.CASCADE,
        related_name='observations' ,
        blank= True ,
        null = True ,

    )

# MedicationAdministered model
class MedicationAdministered(models.Model):
    id = models.AutoField(primary_key=True)
    care_provided = models.ForeignKey(
        CareProvided,
        on_delete=models.CASCADE,
        related_name='medications_administered'
    )
    medicine = models.OneToOneField(
        'Medecine',
        on_delete=models.CASCADE
    )

class BiologicalAssessment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    patient_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    tests_to_conduct = models.TextField()  # Liste des tests à réaliser

    ehr = models.ForeignKey(
        EHR,  # Relier avec l'EHR du patient
        on_delete=models.CASCADE,
        related_name='biological_assessments'
    )

    # Lien avec le médecin qui effectue l'évaluation
    doctor = models.ForeignKey(
        Doctor,  # Relier avec le modèle Doctor
        on_delete=models.CASCADE,  # Si le médecin est supprimé, supprimer les évaluations biologiques associées
        related_name='biological_assessments',  # Permet d'accéder aux évaluations biologiques du médecin
        null=True,  # Rendre ce champ optionnel
        blank=True  # Rendre ce champ optionnel dans le formulaire
    )
    # Mandatory One-to-One Relationship with BiologyReport
    biology_report = models.OneToOneField(
        BiologyReport,  # Linking to BiologyReport model
        on_delete=models.CASCADE,  # Deleting the assessment also deletes the related report
        related_name='assessment',  # Allows reverse lookup from BiologyReport
        null=True,  
        blank=True
    )

class RadiologyAssessment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    patient_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    imaging_type = models.CharField(max_length=255)  # Type d'imagerie (IRM, Scanner, etc.)

    ehr = models.ForeignKey(
        EHR,  # Relier avec l'EHR du patient
        on_delete=models.CASCADE,
        related_name='radiology_assessments'
    )

    # Lien avec le médecin qui effectue l'évaluation
    doctor = models.ForeignKey(
        Doctor,  # Relier avec le modèle Doctor
        on_delete=models.CASCADE,  # Si le médecin est supprimé, supprimer les évaluations biologiques associées
        related_name='radiology_assessments',  # Permet d'accéder aux évaluations biologiques du médecin
        null=True,  # Rendre ce champ optionnel
        blank=True  # Rendre ce champ optionnel dans le formulaire
    )

# Mandatory One-to-One Relationship with RadiologyReport
    radiology_report = models.OneToOneField(
        RadiologyReport,  # Linking to RadiologyReport model
        on_delete=models.CASCADE,  # Deleting the assessment also deletes the related report
        related_name='assessment',  # Allows reverse lookup from RadiologyReport
        null=True,  
        blank=True
    )

from django.db import models

class sgph(models.Model):

    email = models.CharField(max_length=70)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=50, default='sgph')
   