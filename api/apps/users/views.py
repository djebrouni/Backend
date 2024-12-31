import json
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
                "occupation": role,
            }
        else:
            return JsonResponse({'error': 'Role not recognized'}, status=400)

        return JsonResponse(profile_data, status=200)

    @verify_user
    def patchUser(self, request, *args, **kwargs):
        # Get the role and user from the request
        role = request.role
        user = request.user

        try:
            # Parse the JSON body
            data = json.loads(request.body)

            # Update fields for the user
            updatable_fields = {
                "name": data.get("name"),
                "surname": data.get("surname"),
                "email": data.get("email"),
                "phoneNumber": data.get("phoneNumber"),
            }

            # Filter out None values to avoid overwriting existing data
            for field, value in updatable_fields.items():
                if value is not None:
                    setattr(user, field, value)

            # Save the updated user object to the database
            user.save()

            return JsonResponse({"message": "User profile updated successfully."}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
     