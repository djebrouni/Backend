from rest_framework import serializers
from .models import Patient

class PatientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'nss', 'name', 'surname','dateofbirth' ,'adress','email', 'phone', 'mutual','password', 'contactperson', 'bloodtype', 'hospital_idHospital']
