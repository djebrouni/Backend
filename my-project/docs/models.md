# Documentation des Modèles

## Table des Matières
1. [EHR](#EHR)
2. [Doctor](#Doctor)
3. [Hospital](#Hospital)
4. [Patient](#Patient)
5. [Administratif Staff](#Administratif-Staff)
6. [LabTechnician](#LabTechnician)
7. [Diagnostic](#Diagnostic)
8. [Consultation](#Consultation)
9. [Medecine](#Medecine)
10. [MedicalCertificate](#MedicalCertificate)
11. [Prescription](#Prescription)
12. [MedicalTreatment](#MedicalTreatment)
13. [Nurse](#Nurse)
14. [Radiologist](#Radiologist)
15. [RadiologyReport](#RadiologyReport)
16. [BiologyReport](#BiologyReport)
17. [CareProvided](#CareProvided)
18. [Observation](#Observation)
19. [MedicationAdministered](#MedicationAdministered)
20. [BiologicalAssessment](#BiologicalAssessment)
21. [RadiologyAssessment](#RadiologyAssessment)
22. [Sgph](#Sgph)

---

## EHR

- **id** : `AutoField, primary_key=True`
- **creator** : `ForeignKey(Doctor)`, Lié à un médecin
- **creator_staff** : `ForeignKey(administratifStaff)`, Lié à un membre du personnel administratif

## Doctor

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`
- **surname** : `CharField(max_length=45)`
- **phoneNumber** : `CharField(max_length=10)`
- **specialization** : `CharField(max_length=45)`
- **email** : `CharField(max_length=70)`
- **password** : `CharField(max_length=200)`
- **role** : `CharField(max_length=50, default='doctor')`
- **ehr** : `ManyToManyField(EHR)`, Lien vers les EHR

## Hospital

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`

## Patient

- **id** : `AutoField, primary_key=True`
- **NSS** : `CharField(max_length=255, unique=True)`
- **name** : `CharField(max_length=45)`
- **surname** : `CharField(max_length=45)`
- **dateOfBirth** : `DateField(null=True)`
- **address** : `CharField(max_length=70, blank=True)`
- **phoneNumber** : `CharField(max_length=10, blank=True)`
- **mutual** : `CharField(max_length=45, blank=True)`
- **contactPerson** : `CharField(max_length=45, blank=True)`
- **bloodType** : `CharField(max_length=11, choices=BloodType)`
- **gender** : `CharField(max_length=15, blank=True)`
- **email** : `EmailField(blank=True, null=True)`
- **profession** : `CharField(max_length=100, blank=True, null=True)`
- **password** : `CharField(max_length=255, null=True, blank=True)`
- **role** : `CharField(max_length=50, default=ROLES.Patient.value)`
- **ehr** : `OneToOneField(EHR)`, Lien vers un EHR
- **hospital** : `ForeignKey(Hospital)`

## Administratif Staff

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`
- **surname** : `CharField(max_length=45)`
- **phoneNumber** : `CharField(max_length=10)`
- **email** : `CharField(max_length=70)`
- **password** : `CharField(max_length=200)`
- **role** : `CharField(max_length=50, default='administratifStaff')`

## LabTechnician

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`
- **surname** : `CharField(max_length=45)`
- **phoneNumber** : `CharField(max_length=10)`
- **specialization** : `CharField(max_length=45)`
- **email** : `CharField(max_length=70)`
- **password** : `CharField(max_length=200)`
- **role** : `CharField(max_length=50, default='LabTechnician')`

## Diagnostic

- **id** : `AutoField, primary_key=True`
- **prescription** : `OneToOneField(Prescription)`

## Consultation

- **id** : `AutoField, primary_key=True`
- **date** : `DateField()`
- **summary** : `TextField()`
- **chiefComplaint** : `TextField()`
- **done** : `BooleanField(default=False)`
- **diagnostic** : `OneToOneField(Diagnostic)`

## Medecine

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`

## MedicalCertificate

- **id** : `AutoField, primary_key=True`
- **requesed** : `BooleanField(default=False)`
- **doctor** : `ForeignKey(Doctor)`
- **ehr** : `ForeignKey(EHR)`

## Prescription

- **id** : `AutoField, primary_key=True`
- **isValid** : `BooleanField(default=False)`
- **date** : `DateField(auto_now_add=True)`
- **doctor** : `ForeignKey(Doctor)`
- **ehr** : `ForeignKey(EHR)`

## MedicalTreatment

- **dose** : `FloatField(validators=[MinValueValidator(0)])`
- **Duration** : `IntegerField(default=0)`
- **medicine** : `OneToOneField(Medecine)`
- **prescription** : `ForeignKey(Prescription)`

## Nurse

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`
- **surname** : `CharField(max_length=45)`
- **phoneNumber** : `CharField(max_length=10)`
- **email** : `CharField(max_length=70)`
- **password** : `CharField(max_length=200)`
- **role** : `CharField(max_length=50, default='Nurse')`
- **ehr** : `ManyToManyField(EHR)`

## Radiologist

- **id** : `AutoField, primary_key=True`
- **name** : `CharField(max_length=45)`
- **surname** : `CharField(max_length=45)`
- **phoneNumber** : `CharField(max_length=10)`
- **specialization** : `CharField(max_length=45)`
- **email** : `CharField(max_length=70)`
- **password** : `CharField(max_length=200)`
- **role** : `CharField(max_length=50, default='Radiologist')`

## RadiologyReport

- **id** : `AutoField, primary_key=True`
- **Type** : `CharField(max_length=45)`
- **imageData** : `ImageField(upload_to='radiology_reports/')`
- **date** : `DateField()`
- **description** : `TextField()`
- **doctor** : `ForeignKey(Doctor)`
- **radiologist** : `ForeignKey(Radiologist)`
- **ehr** : `ForeignKey(EHR)`

## BiologyReport

- **id** : `AutoField, primary_key=True`
- **bloodSugarLevel** : `FloatField()`
- **bloodPressure** : `FloatField()`
- **cholesterolLevel** : `FloatField()`
- **completeBloodCount** : `FloatField()`
- **doctor** : `ForeignKey(Doctor)`
- **lab_technician** : `ForeignKey(LabTechnician)`
- **ehr** : `ForeignKey(EHR)`
- **date** : `DateField(auto_now_add=True)`

## CareProvided

- **id** : `AutoField, primary_key=True`
- **date** : `DateField()`
- **time** : `TimeField()`
- **care_actions** : `TextField()`
- **nurse** : `ForeignKey(Nurse)`
- **ehr** : `ForeignKey(EHR)`

## Observation

- **id** : `AutoField, primary_key=True`
- **description** : `TextField()`
- **care_provided** : `ForeignKey(CareProvided)`

## MedicationAdministered

- **id** : `AutoField, primary_key=True`
- **care_provided** : `ForeignKey(CareProvided)`
- **medicine** : `OneToOneField(Medecine)`

## BiologicalAssessment

- **id** : `AutoField, primary_key=True`
- **date** : `DateField()`
- **patient_name** : `CharField(max_length=100)`
- **date_of_birth** : `DateField()`
- **age** : `IntegerField()`
- **gender** : `CharField(max_length=10)`
- **tests_to_conduct** : `TextField()`
- **ehr** : `ForeignKey(EHR)`
- **doctor** : `ForeignKey(Doctor)`
- **biology_report** : `OneToOneField(BiologyReport)`

## RadiologyAssessment

- **id** : `AutoField, primary_key=True`
- **date** : `DateField()`
- **patient_name** : `CharField(max_length=100)`
- **date_of_birth** : `DateField()`
- **age** : `IntegerField()`
- **gender** : `CharField(max_length=10)`
- **imaging_type** : `CharField(max_length=255)`
- **ehr** : `ForeignKey(EHR)`
- **doctor** : `ForeignKey(Doctor)`
- **radiology_report** : `OneToOneField(RadiologyReport)`

## Sgph

- **email** : `CharField(max_length=70)`
- **password** : `CharField(max_length=200)`
- **role** : `CharField(max_length=50, default='sgph')`
