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

from api.const.ROLES import ROLES
from api.models import administratifStaff, Doctor, LabTechnician, Nurse, Patient, Radiologist

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


class SignUpView(APIView):
    def post(self, request):
        # get model
        print('HH')
        role = request.data.get('role')
        Model = getModel(role.capitalize())
        if not Model:
            return JsonResponse({'message': 'Role does not exist'}, status=400)        
        
        # Extract data from the request
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        surname = request.data.get('surname')
        
        if role.capitalize() == ROLES.Patient.value:
            nss = request.data.get('nss')
            # date_of_birth = request.data.get('dateOfBirth')
            # address = request.data.get('address')
            # phone_number = request.data.get('phoneNumber')
            # mutual = request.data.get('mutual')
            # contact_person = request.data.get('contactPerson')
            # blood_type = request.data.get('bloodType')
            # gender = request.data.get('gender')
            # profession = request.data.get('profession')
            # hospital_id = request.data.get('hospital')
            
            # Check if patient with NSS already exists
            existing_user = Model.objects.filter(NSS=nss).first()
            if existing_user:
                return Response({'message': 'An account with this NSS already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            

        # Validate email
        # email_validation = self.validate_email(email)
        # if email_validation == 'disposable':
        #     return Response({'message': 'Temporary email addresses are not allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        # elif email_validation == 'risky':
        #     return Response({'message': 'The email address does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        # elif email_validation == 'invalid':
        #     return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Check if patient with email already exists
        existing_user = Patient.objects.filter(email=email).first()
        if existing_user:
            return Response({'message': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # create user
        user = Model(
            email=email,
            password=password,
            name=name,
            surname=surname,
        )
        
        if role.capitalize() == ROLES.Patient.value:
            user.NSS = nss
        
        # save
        user.save()
        
        # end
        return Response({'message': 'Account created successfully.'}, status=status.HTTP_200_OK)

        
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


# @method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        role = data.get('role')
        Model = getModel(role.capitalize())
        if not Model:
            return JsonResponse({'message': 'Role does not exist'}, status=400)        
        
        # get data
        email = data.get('email')
        password = data.get('password')
        
        # Recherche dans le modèle
        try:
            user = Model.objects.get(email=email)
        except:
            return JsonResponse({'message': 'Email ou mot de passe invalide.'}, status=400)
        
        # check mdp
        
        if check_password(password, user.password):
            return JsonResponse({'message': 'Email ou mot de passe invalide.'}, status=400)
       
        # Générer un token JWT
        payload = {
            'user_id': user.id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse({
            'message': 'Authentification réussie !',
            'token': token,
        }, status=200)
