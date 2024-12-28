from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from  api.middlewares.authentication import verify_user
from api.helper.getModels import getModel
from api.const.ROLES import ROLES

class UserProfileView(View):

    @verify_user  # Ensure the request is authenticated
    def get(self, request, *args, **kwargs):
        role = request.role
        model = request.Model
        user = request.user
        profile_data = {}

        # Role-based data preparation using ROLES Enum
        if role == ROLES.Patient.value:
            profile_data = {
                "name": user.name,
                "surname": user.surname,
                "NSS" : user.NSS,
                "currentHospital": user.hospital.name if user.hospital else None,
                "specialization": user.specialization,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
            }

        elif role == ROLES.Medecin.value:
            profile_data = {
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "specialization": user.specialization,
                "occupation": ROLES.Medecin.value,

            }

        elif role == ROLES.Infirmier.value:
            profile_data = {
               "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "specialization": user.specialization,
                "occupation": ROLES.Infirmier.value,

            }

        elif role == ROLES.Radiologue.value:
            profile_data = {
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "specialization": user.specialization,
                "occupation": ROLES.Radiologue.value,

            }

        elif role == ROLES.Laboratin.value:
            profile_data = {
               "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "specialization": user.specialization,
                "occupation": ROLES.Laboratin.value,

            }

        elif role == ROLES.Personnel.value:
            profile_data = {
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "specialization": user.specialization,
                "occupation": ROLES.Personnel.value,

            }

        else:
            return JsonResponse({'error': 'Role not recognized'}, status=400)

        return JsonResponse(profile_data, status=200)
