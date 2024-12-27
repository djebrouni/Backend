import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSignupSerializer
from .models import Patient
class PatientSignupView(APIView):
    def post(self, request):
        # Extract email and NSS from the request data
        email = request.data.get('email')
        nss = request.data.get('nss')  # Assuming nss is passed in the request data
        name = request.data.get('name')
        surname = request.data.get('surname')
        password = request.data.get('password')
        
        # Email validation
        email_validation = self.validate_email(email)

        if email_validation == 'disposable':
            return Response({'message': 'Temporary email addresses are not allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        elif email_validation == 'risky':
            return Response({'message': 'The email address does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        elif email_validation == 'invalid':
            return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a patient with the same NSS exists
        existing_patient = Patient.objects.filter(nss=nss).first()

        if existing_patient:
            # If the patient exists and has a non-null email and password, reject the signup (duplicate account)
            if existing_patient.email and existing_patient.password:
                return Response({'message': 'An account with this NSS and email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # If the patient exists but has an empty email or password, update the record
            if not existing_patient.email and not existing_patient.password:
                existing_patient.email = email
                existing_patient.password = request.data.get('password')  # Assuming the password is passed in the request
                existing_patient.save()
                return Response({'message': 'Patient account updated successfully with email and password.'}, status=status.HTTP_200_OK)

        # If no patient exists with this NSS, return the message 'Your EHR is not created yet'
        return Response({'message': 'Your EHR is not created yet.'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the patient signup if the email is valid and no duplicates were found
        serializer = PatientSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Patient registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
