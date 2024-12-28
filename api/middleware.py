import jwt
from django.http import JsonResponse
from django.conf import settings
from .models import administratifStaff, Doctor, LabTechnician, Nurse, Patient, Radiologist

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

                # Récupérer le rôle et l'utilisateur
                role = payload.get('role')
                user_id = payload.get('user_id')

                # Vérifier l'utilisateur en fonction du rôle
                if role == 'admin':
                    request.user = administratifStaff.objects.get(id=user_id)
                elif role == 'doctor':
                    request.user = Doctor.objects.get(id=user_id)
                elif role == 'lab_technician':
                    request.user = LabTechnician.objects.get(id=user_id)
                elif role == 'nurse':
                    request.user = Nurse.objects.get(id=user_id)
                elif role == 'patient':
                    request.user = Patient.objects.get(id=user_id)
                elif role == 'radiologist':
                    request.user = Radiologist.objects.get(id=user_id)
                else:
                    return JsonResponse({'message': 'Rôle invalide.'}, status=401)

            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
                return JsonResponse({'message': 'Token invalide ou expiré.'}, status=401)

        response = self.get_response(request)
        return response
