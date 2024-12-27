from django.db import models

class Patient(models.Model):
    idPatient = models.AutoField(primary_key=True)  # Matches idPatient
    nss = models.CharField(max_length=45, unique=True)  # NSS must be unique
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    dateofbirth = models.CharField(max_length=45, blank=True, null=True)
    password =models.CharField(max_length=45, blank=True, null=True)
    adress = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    mutual = models.CharField(max_length=45, blank=True, null=True)
    contactperson = models.CharField(max_length=45, blank=True, null=True)
    bloodtype = models.CharField(max_length=45, blank=True, null=True)
    hospital_idHospital = models.IntegerField(blank=True ,null=False)  # Matches Hospital_idHospital
    email =models.CharField(max_length=45)

    class Meta:
        db_table = 'patient'  # Ensure Django uses the 'patient' table from your database

    def __str__(self):
        return f"{self.name} {self.surname}"
