from django.db import models

# EHR model
class EHR(models.Model):
    idEHR = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    administrativeStaff = models.ForeignKey(
        'AdminitratifStaff',  # Foreign key to the AdminitratifStaff model (you need to define it)
        on_delete=models.CASCADE
    )
    # Other EHR-related fields, e.g.:
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'EHR #{self.idEHR}'


# Patient model
class Patient(models.Model):
    idPatient = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    NSS = models.PositiveIntegerField(unique=True)  # National Social Security number, for example
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    dateOfBirth = models.DateField()
    address = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=10)
    mutual = models.CharField(max_length=45)
    contactPerson = models.CharField(max_length=45)
    bloodType = models.CharField(max_length=2)
    gender = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)

    # Linking to the EHR model with a one-to-one relationship
    ehr = models.OneToOneField(
        EHR, 
        on_delete=models.CASCADE, 
        related_name='patient', 
        null=True, 
        blank=True  # Optional: if not all patients have an EHR initially
    )

    # You may need to add the Hospital_idHospital field if relevant

    def __str__(self):
        return f'{self.name} {self.surname}'
