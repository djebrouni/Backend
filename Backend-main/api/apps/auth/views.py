from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.hashers import check_password

from api.models import administratifStaff, Doctor, LabTechnician, Nurse, Patient, Radiologist

class PatientSignupView(APIView):
    def post(self, request):
        # Extract data from the request
        nss = request.data.get('NSS')
        email = request.data.get('email')
        name = request.data.get('name')
        surname = request.data.get('surname')
        date_of_birth = request.data.get('dateOfBirth')
        address = request.data.get('address')
        phone_number = request.data.get('phoneNumber')
        mutual = request.data.get('mutual')
        contact_person = request.data.get('contactPerson')
        blood_type = request.data.get('bloodType')
        gender = request.data.get('gender')
        profession = request.data.get('profession')
        hospital_id = request.data.get('hospital')
        password = request.data.get('password')

        # Validate email
        email_validation = self.validate_email(email)
        if email_validation == 'disposable':
            return Response({'message': 'Temporary email addresses are not allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        elif email_validation == 'risky':
            return Response({'message': 'The email address does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        elif email_validation == 'invalid':
            return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if patient with NSS already exists
        existing_patient = Patient.objects.filter(NSS=nss).first()

        if existing_patient:
            # Check if patient has already registered
            if existing_patient.email and existing_patient.password:
                return Response({'message': 'An account with this NSS and email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            # Update patient record if email or password is missing
            if not existing_patient.email and not existing_patient.password:
                existing_patient.email = email
                existing_patient.password = password
                existing_patient.save()
                return Response({'message': 'Patient account updated successfully.'}, status=status.HTTP_200_OK)

        # If no patient exists, ensure EHR is ready
        return Response({'message': 'Your EHR is not created yet.'}, status=status.HTTP_400_BAD_REQUEST)

    def validate_email(self, email):
        api_key = '487f1407878890e0d0414c2bc1d91a538890a807'  # Replace with your actual Hunter API key
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

        try:
            response = requests.get(url)
            response_data = response.json()
            data = response_data.get('data', {})

            if data.get('status') == 'valid' and not data.get('disposable'):
                return 'valid'
            elif data.get('disposable'):
                return 'disposable'
            elif data.get('risky'):
                return 'risky'
            else:
                return 'invalid'
        except Exception as e:
            print(f"Error validating email: {e}")
            return 'invalid'
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
import datetime
import jwt
from api.helper.getModels import getModel  # Import the getModel function
from django.conf import settings

@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        # Liste des modèles
        models = [
            administratifStaff,
            Doctor,
            LabTechnician,
            Nurse,
            Patient,
            Radiologist
        ]

        user = None

        # Recherche dans chaque modèle
        for model in models:
            try:
                user = model.objects.get(email=email)  # Use get() for single result
                if check_password(password, user.password):
                    # If user is found and password matches, break out of the loop
                    break
            except model.DoesNotExist:
                continue  # User not found in this model, move to the next one

        # Si l'utilisateur n'existe pas
        if not user:
            return JsonResponse({'message': 'Email ou mot de passe invalide.'}, status=400)

        # Assuming the role is a field in each model
        role = getattr(user, 'role', None)  # Use the 'role' attribute from the user object
        
        # Générer un token JWT
        payload = {
            'user_id': user.id,
            'role': role,  # Use the dynamically retrieved role
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({
            'message': 'Authentification réussie !',
            'token': token,
            'role': role
        }, status=200)
