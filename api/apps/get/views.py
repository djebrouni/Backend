from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.const.ROLES import ROLES
from api.models import Doctor, Hospital
from django.conf import settings
import jwt
from api.middlewares.authentication import verify_user
from api.middlewares.authorization import verify_role

class HospitalRecordsView(View):
    verify_user
    verify_role(ROLES.Doctor, ROLES.AdministratifStaff)
    def get(self, request):
        try:
            # Retrieve all hospital records
            records = Hospital.objects.all().values()
            return JsonResponse({"hospitals": list(records)}, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class DoctorRecordsView(View):
    verify_user
    verify_role(ROLES.Doctor, ROLES.AdministratifStaff)
    def get(self, request):
        try:
            # Retrieve all doctor records
            doctors = Doctor.objects.all().values()
            return JsonResponse({"doctors": list(doctors)}, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        


from django.http import JsonResponse

from api.models import Prescription, MedicalTreatment
import jwt
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class PrescriptionDetailView(View):
    def get(self, request, prescription_id):
        # Validate Authorization Token
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # Extract token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Check role
            role = decoded.get("role", "").strip().lower()
           
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        try:
            # Retrieve the specific prescription by ID
            prescription = Prescription.objects.get(id=prescription_id)

            # Fetch treatments linked to this prescription
            treatments = MedicalTreatment.objects.filter(prescription=prescription)

            treatment_list = []
            for treatment in treatments:
                treatment_list.append({
                    "medicine": treatment.medicine.name,
                    "dose": treatment.dose,
                    "duration": treatment.Duration
                })

            # Return prescription details along with treatments
            return JsonResponse({
                "prescription": {
                    "id": prescription.id,
                    "isValid": prescription.isValid,
                    "doctor": f"{prescription.doctor.name} {prescription.doctor.surname}",
                    "date": prescription.date.strftime("%Y-%m-%d"),
                    "ehr": prescription.ehr.id,
                    "treatments": treatment_list
                }
            }, status=200)

        except Prescription.DoesNotExist:
            return JsonResponse({"error": "Prescription not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from api.models import CareProvided, Observation, MedicationAdministered
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import jwt
from django.conf import settings

@method_decorator(csrf_exempt, name='dispatch')
class CareProvidedDetailView(View):
    def get(self, request, care_id):
        # Validate Authorization Token
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # Extract token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Check role
            role = decoded.get("role", "").strip().lower()
           
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        try:
            # Retrieve care provided for the given care_id
            try:
                care = CareProvided.objects.get(id=care_id)
            except CareProvided.DoesNotExist:
                return JsonResponse({"error": "Care provided not found"}, status=404)

            # Fetch observations related to the care provided
            observations = Observation.objects.filter(care_provided=care).values()

            # Fetch administered medications related to the care provided
            medications = MedicationAdministered.objects.filter(care_provided=care).values()

            # Prepare care provided data
            care_provided_data = {
                'id': care.id,
                'date': care.date,
                'time': care.time.strftime("%H:%M:%S"),
                'care_actions': care.care_actions,
                'observations': list(observations),
                'administered_medications': list(medications)
            }

            # Return care provided data
            return JsonResponse({"care_provided": care_provided_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
