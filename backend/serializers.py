from rest_framework import serializers
from .models import Patient

class PatientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['idPatient', 'nss', 'name', 'surname', 'dateofbirth', 'adress', 'phone', 'mutual', 'contactperson', 'bloodtype', 'Hospital_idHospital']
