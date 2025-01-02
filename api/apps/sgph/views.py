from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from api.models import Prescription, MedicalTreatment
import json
import jwt
from django.conf import settings


@method_decorator(csrf_exempt, name='dispatch')
class ValidatePrescriptionView(View):
    def post(self, request):
        # Validate Token
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # Assuming Bearer token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()

            # Check if the role is 'sgph'
            if role != 'sgph':
                return JsonResponse({"error": "Unauthorized role"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        # Process Prescription Validation
        try:
            data = json.loads(request.body.decode('utf-8'))
            prescription_id = data.get('prescription_id')

            if not prescription_id:
                return JsonResponse({"error": "Missing 'prescription_id' parameter"}, status=400)

            # Fetch the prescription
            prescription = Prescription.objects.get(id=prescription_id)

            

            # Mark prescription as valid
            prescription.isValid = True
            prescription.save()

            return JsonResponse({"message": "Prescription validated successfully."}, status=200)

        except Prescription.DoesNotExist:
            return JsonResponse({"error": "Prescription not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.models import Prescription, MedicalTreatment
from django.core.serializers import serialize
import jwt
from django.conf import settings

@method_decorator(csrf_exempt, name='dispatch')
class PrescriptionListView(View):
    def get(self, request):
        # Validate Authorization Token
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # Extract token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Check role
            role = decoded.get("role", "").strip().lower()
            if role not in ['doctor', 'nurse', 'administratifstaff', 'sgph']:
                return JsonResponse({"error": "Unauthorized role"}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        try:
            # Retrieve all prescriptions with details
            prescriptions = Prescription.objects.all()
            prescription_list = []

            for prescription in prescriptions:
                # Fetch treatments linked to this prescription
                treatments = MedicalTreatment.objects.filter(prescription=prescription)

                treatment_list = []
                for treatment in treatments:
                    treatment_list.append({
                        "medicine": treatment.medicine.name,
                        "dose": treatment.dose,
                        "duration": treatment.Duration
                    })

                # Append prescription details
                prescription_list.append({
                    "id": prescription.id,
                    "isValid": prescription.isValid,
                    "doctor": f"{prescription.doctor.name} {prescription.doctor.surname}",
                    "date": prescription.date.strftime("%Y-%m-%d"),
                    "ehr": prescription.ehr.id,
                    "treatments": treatment_list
                })

            # Return all prescriptions
            return JsonResponse({"prescriptions": prescription_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
