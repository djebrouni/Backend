import json
import jwt
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localdate
from api.models import Patient, EHR, Radiologist, RadiologyAssessment, Consultation, Diagnostic, BiologicalAssessment, BiologyReport, LabTechnician, Doctor,RadiologyAssessment, RadiologyReport, Radiologist
from django.contrib.auth.models import User
import jwt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.models import BiologicalAssessment, Doctor
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import jwt
from django.conf import settings
from api.models import EHR, Prescription, MedicalTreatment, Medecine, Doctor, Patient
from django.shortcuts import get_object_or_404
from django.db import transaction
import re
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist




def rechercheDpiParNss(request):
    # Ensure the method is GET
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)

    token = token.split(" ")[1]  # Assuming Bearer Token

    try:
        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Validate role
        valid_roles = ['doctor', 'administratifstaff']
        if role not in valid_roles:
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    

    try:

        # Parse JSON input
        data = json.loads(request.body.decode('utf-8'))
        nss = data.get('nss')

        if not nss:
            return JsonResponse({"error": "Missing 'nss' parameter"}, status=400)
        # Search for the patient using NSS
        patient = Patient.objects.get(NSS=nss)
        ehr = EHR.objects.get(patient=patient)

        # Return the EHR ID and patient details
        return JsonResponse({
            'ehr_id': ehr.id,
            'name': patient.name,
            'surname': patient.surname,
            'nss': patient.NSS
        })
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)
    except EHR.DoesNotExist:
        return JsonResponse({'error': 'EHR not found for this patient'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')  # Désactive la vérification CSRF
class ConsultationSummaryView(View):
    def get(self, request, consultation_id):
        # Vérification du token JWT
        error_response = validate_user_token(request)
        if error_response:  # Si le token est invalide ou manquant
            return error_response

        try:
            # Récupérer l'objet Consultation existant
            consultation = Consultation.objects.get(id=consultation_id)

            # Inclure le diagnostic dans la réponse
            diagnostic_id = consultation.diagnostic.id if consultation.diagnostic else None

            # Retourner le résumé (summary) de la consultation et l'ID du diagnostic
            return JsonResponse({
                'summary': consultation.summary,
                'diagnostic_id': diagnostic_id
            }, status=200)

        except Consultation.DoesNotExist:
            return JsonResponse({'error': 'Consultation not found'}, status=404)


def validate_user_token(request):
    """
    Validate the Authorization token.
    """
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)
    try:
        # Extract and decode the token
        token = token.split(" ")[1]  # Assuming Bearer Token
        jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return None  # Token is valid
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
def get_user_role_from_token(request):
    """
    Extrait le rôle de l'utilisateur à partir du token d'autorisation.
    """
    token = request.headers.get("Authorization")
    if not token:
        return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
    try:
        # Extraire et décoder le token
        token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded.get("role", "").strip().lower(), None
    except jwt.ExpiredSignatureError:
        return None, JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return None, JsonResponse({"error": "Invalid token"}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class ConsultationCreateView(View):
    def post(self, request):
        # Check user role
        role, error_response = get_user_role_from_token(request)
        if error_response:
            return error_response
        if role != "doctor":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        try:
            # Parse the JSON request
            data = json.loads(request.body)

            # Extract fields
            date = data.get('date')
            summary = data.get('summary')
            chief_complaint = data.get('chief_complaint')

            # Create a new diagnostic
            diagnostic = Diagnostic.objects.create()

            # Create consultation and associate diagnostic
            consultation = Consultation.objects.create(
                date=date,
                summary=summary,
                chiefComplaint=chief_complaint,
                diagnostic=diagnostic
            )

            return JsonResponse({
                'consultation_id': consultation.id,
                'diagnostic_id': diagnostic.id,
                'message': 'Consultation and Diagnostic created successfully'
            }, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ConsultationUpdateView(View):
    def post(self, request, consultation_id):
        # Check user role
        role, error_response = get_user_role_from_token(request)
        if error_response:
            return error_response
        if role != "doctor":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        try:
            # Parse the JSON request
            data = json.loads(request.body)

            # Extract fields
            summary = data.get('summary')
            chief_complaint = data.get('chief_complaint')

            # Retrieve and update consultation
            consultation = Consultation.objects.get(id=consultation_id)
            consultation.summary = summary if summary else consultation.summary
            consultation.chiefComplaint = chief_complaint if chief_complaint else consultation.chiefComplaint
            consultation.save()

            return JsonResponse({'message': 'Consultation updated successfully'}, status=200)

        except Consultation.DoesNotExist:
            return JsonResponse({'error': 'Consultation not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::CREATION DU BILAN ASSESMET ET SON DISPLAY:::::::::::::::::::::::::::::::::::::::


@method_decorator(csrf_exempt, name='dispatch')
class CreateBiologicalAssessmentView(View):
    def get_doctor_from_token(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # On suppose que le token est de type 'Bearer <token>'
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get('user_id')
            role = decoded.get('role')

            if not user_id:
                return None, JsonResponse({"error": "User ID not found in token"}, status=401)
            
            if role != 'doctor':
                return None, JsonResponse({"error": "Unauthorized role, not a doctor"}, status=403)

            doctor = get_object_or_404(Doctor, id=user_id)
            return doctor, None
        
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def calculate_age(self, date_of_birth):
        today = localdate()  # Utilise la date locale du serveur
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def post(self, request, ehr_id):
        # Extraire les informations du médecin via le token
        doctor, error_response = self.get_doctor_from_token(request)
        if error_response:
            return error_response

        # Récupérer l'EHR du patient avec l'ehr_id
        ehr = get_object_or_404(EHR, id=ehr_id)

        # Récupérer le patient associé à cet EHR
        patient = ehr.patient  # On accède à l'objet Patient grâce à la relation OneToOne

        # Extraire les informations du patient depuis le modèle Patient
        patient_name = f"{patient.name} {patient.surname}"
        date_of_birth = patient.dateOfBirth.strftime("%Y-%m-%d")  # Formater la date de naissance
        gender = patient.gender

        # Calculer l'âge en fonction de la date de naissance
        age = self.calculate_age(date_of_birth)

        # Récupérer les tests à conduire depuis le corps de la requête
        data = json.loads(request.body)
        tests_to_conduct = data.get('tests_to_conduct')

        # Validation des champs requis
        if not tests_to_conduct:
            return JsonResponse({"error": "Missing 'tests_to_conduct' field"}, status=400)

        # Créer un BiologyReport vide
        biology_report = BiologyReport.objects.create(
            bloodSugarLevel=0,  # Valeur par défaut pour le niveau de sucre dans le sang
            bloodPressure=0,  # Valeur par défaut pour la pression artérielle
            cholesterolLevel=0,  # Valeur par défaut pour le niveau de cholestérol
            completeBloodCount=0 ,
            doctor=doctor,  # Associe le rapport au médecin
            ehr=ehr  # Lien avec l'EHR
            
        )

        # Créer l'évaluation biologique et l'associer au médecin et au patient via l'EHR
        biological_assessment = BiologicalAssessment.objects.create(
            date=datetime.now().strftime("%Y-%m-%d"),
            patient_name=patient_name,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            tests_to_conduct=tests_to_conduct,
            ehr=ehr,
            doctor=doctor,  # Associer l'évaluation biologique au médecin
            biology_report=biology_report  # Lier l'évaluation au rapport biologique
        )

        return JsonResponse({
            'message': 'Biological assessment created successfully',
            'assessment_id': biological_assessment.id,
            'biology_report_id': biology_report.id
        })
@method_decorator(csrf_exempt, name='dispatch')
class DisplayBiologicalAssessmentView(View):
    def authenticate_user(self, request):
        # Extraire le token de la requête
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # On suppose que le token est de type 'Bearer <token>'
            jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return True, None
        except jwt.ExpiredSignatureError:
            return False, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return False, JsonResponse({"error": "Invalid token"}, status=401)

    def get(self, request, ehr_id):
        # Authentification de l'utilisateur
        is_authenticated, error_response = self.authenticate_user(request)
        if not is_authenticated:
            return error_response

        # Récupérer l'EHR du patient
        ehr = get_object_or_404(EHR, id=ehr_id)

        # Récupérer les évaluations biologiques associées à cet EHR
        biological_assessments = BiologicalAssessment.objects.filter(ehr=ehr)

        # Vérifier si des évaluations biologiques existent
        if not biological_assessments:
            return JsonResponse({"error": "No biological assessments found for this EHR ID"}, status=404)

        # Structurer les données pour la réponse JSON
        response_data = []
        for assessment in biological_assessments:
            response_data.append({
                "date": assessment.date,
                "patient_name": assessment.patient_name,
                "date_of_birth": assessment.date_of_birth,
                "age": assessment.age,
                "gender": assessment.gender,
                "tests_to_conduct": assessment.tests_to_conduct,
                "doctor_name": f"{assessment.doctor.name} {assessment.doctor.surname}" if assessment.doctor else "Unknown Doctor",
            })

        return JsonResponse(response_data, safe=False, status=200)

#:::::::::::::::::::::::::::::::::::::::::::CREATION RADIOLOGY ASSESMEENT ET SON DISPLAY::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@method_decorator(csrf_exempt, name='dispatch')
class CreateRadiologyAssessmentView(View):
    def get_doctor_from_token(self, request):
        """
        Extrait le médecin à partir du token d'autorisation.
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get('user_id')
            role = decoded.get('role')
            if not user_id:
                return None, JsonResponse({"error": "User ID not found in token"}, status=401)
            if role != 'doctor':
                return None, JsonResponse({"error": "Unauthorized role, not a doctor"}, status=403)
            doctor = get_object_or_404(Doctor, id=user_id)
            return doctor, None
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def post(self, request, ehr_id):
        doctor, error_response = self.get_doctor_from_token(request)
        if error_response:
            return error_response

        ehr = get_object_or_404(EHR, id=ehr_id)
        patient = ehr.patient
        patient_name = f"{patient.name} {patient.surname}"
        date_of_birth = patient.dateOfBirth.strftime("%Y-%m-%d")
        gender = patient.gender
        age = self.calculate_age(patient.dateOfBirth)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        imaging_type = data.get('imaging_type')
        if not imaging_type:
            return JsonResponse({"error": "Missing required field: imaging_type"}, status=400)

        # Création de l'évaluation radiologique
        radiology_assessment = RadiologyAssessment.objects.create(
            date=datetime.now().strftime("%Y-%m-%d"),
            patient_name=patient_name,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            imaging_type=imaging_type,
            ehr=ehr,
            doctor=doctor
        )

        # Création d'un rapport radiologique vide lié à l'évaluation
        radiology_report = RadiologyReport.objects.create(
            Type="",
            imageData=b"",  # Données binaires vides
            date=datetime.now().strftime("%Y-%m-%d"),
            description="",
            doctor=doctor,
            ehr=ehr
        )

        # Lier le rapport radiologique à l'évaluation
        radiology_assessment.radiology_report = radiology_report
        radiology_assessment.save()

        return JsonResponse({
            'message': 'Radiology assessment and empty report created successfully',
            'assessment_id': radiology_assessment.id,
            'report_id': radiology_report.id
        })

    def calculate_age(self, birth_date):
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


@method_decorator(csrf_exempt, name='dispatch')
class DisplayRadiologyAssessmentView(View):
    def authenticate_user(self, request):
        # Vérification du token d'authentification
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # On suppose un Bearer Token
            jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return True, None
        except jwt.ExpiredSignatureError:
            return False, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return False, JsonResponse({"error": "Invalid token"}, status=401)

    def get(self, request, ehr_id):
        # Authentification de l'utilisateur avec le token
        is_authenticated, error_response = self.authenticate_user(request)
        if not is_authenticated:
            return error_response

        # Récupérer les évaluations radiologiques associées à l'EHR donné
        radiology_assessments = RadiologyAssessment.objects.filter(ehr_id=ehr_id)

        # Vérification s'il existe des évaluations radiologiques
        if not radiology_assessments:
            return JsonResponse({"error": "No radiology assessments found for this EHR ID"}, status=404)

        # Structurer les données pour la réponse JSON
        response_data = []
        for assessment in radiology_assessments:
            assessment_data = {
                "id": assessment.id,
                "date": assessment.date.strftime("%Y-%m-%d"),
                "patient_name": assessment.patient_name,
                "date_of_birth": assessment.date_of_birth.strftime("%Y-%m-%d"),
                "age": assessment.age,
                "gender": assessment.gender,
                "imaging_type": assessment.imaging_type,
                "doctor_name": f"{assessment.doctor.name} {assessment.doctor.surname}" if assessment.doctor else "Unknown Doctor",
                "has_radiology_report": assessment.radiology_report is not None  # Indication de la présence d'un rapport
            }

            response_data.append(assessment_data)

        # Retourner les données sous forme de JSON
        return JsonResponse(response_data, safe=False, status=200)



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::REMPLIR LE BILAN ET SON DISPLAY::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@method_decorator(csrf_exempt, name='dispatch')
class FillBiologyReportView(View):
    def get_user_role_from_token(self, request):
        """
        Extrait le rôle de l'utilisateur à partir du token d'autorisation.
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()  
            return role, None
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def post(self, request, assessment_id):
        # Vérifier le rôle de l'utilisateur
        role, error_response = self.get_user_role_from_token(request)
        if error_response:
            return error_response

        if role != "labtechnician":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        # Récupérer les données 
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Extraction des données
        blood_sugar_level = data.get('bloodSugarLevel')
        blood_pressure = data.get('bloodPressure')
        cholesterol_level = data.get('cholesterolLevel')
        complete_blood_count = data.get('completeBloodCount')

        # Validation des champs requis
        if not all([blood_sugar_level, blood_pressure, cholesterol_level, complete_blood_count]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Récupérer l'évaluation biologique (BiologicalAssessment)
        biological_assessment = get_object_or_404(BiologicalAssessment, id=assessment_id)

        # Vérifier si un rapport biologique est déjà associé
        biology_report = biological_assessment.biology_report
        if not biology_report:
            return JsonResponse({"error": "No biology report associated with this assessment"}, status=400)

        # Vérifier si le rapport a déjà été rempli
        if biology_report.bloodSugarLevel or biology_report.bloodPressure or biology_report.cholesterolLevel or biology_report.completeBloodCount:
            return JsonResponse({"error": "This biology report has already been filled"}, status=400)

        # Récupérer le technicien de laboratoire
        lab_technician = LabTechnician.objects.first()  # À adapter selon votre logique

        # Mettre à jour les informations du rapport biologique
        biology_report.bloodSugarLevel = blood_sugar_level
        biology_report.bloodPressure = blood_pressure
        biology_report.cholesterolLevel = cholesterol_level
        biology_report.completeBloodCount = complete_blood_count
        biology_report.lab_technician = lab_technician
        biology_report.save()

        return JsonResponse({
            'message': 'Biology report filled successfully',
            'report_id': biology_report.id
        })
    
@method_decorator(csrf_exempt, name='dispatch')
class DisplayBiologyReportsView(View):
    def get_user_from_token(self, request):
        """
        Extraire l'ID de l'utilisateur à partir du token d'autorisation sans contrainte de rôle.
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get('user_id')

            if not user_id:
                return None, JsonResponse({"error": "User ID not found in token"}, status=401)

            return user_id, None
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def get(self, request, assessment_id):
        # Vérifier l'utilisateur via le token (sans contrainte de rôle)
        user_id, error_response = self.get_user_from_token(request)
        if error_response:
            return error_response

        # Récupérer l'évaluation biologique avec l'ID
        assessment = get_object_or_404(BiologicalAssessment, id=assessment_id)

        # Récupérer le rapport biologique associé à cette évaluation
        biology_report = assessment.biology_report

        if not biology_report:
            return JsonResponse({"error": "No biology report found for this assessment"}, status=404)

        # Format des données à afficher
        report_data = {
            'id': biology_report.id,
            'bloodSugarLevel': biology_report.bloodSugarLevel,
            'bloodPressure': biology_report.bloodPressure,
            'cholesterolLevel': biology_report.cholesterolLevel,
            'completeBloodCount': biology_report.completeBloodCount,
            'doctor': f"{biology_report.doctor.name} {biology_report.doctor.surname}" if biology_report.doctor else None,
            'labTechnician': f"{biology_report.lab_technician.name} {biology_report.lab_technician.surname}" if biology_report.lab_technician else None,
        }

        return JsonResponse({
            'message': 'Biology report retrieved successfully',
            'report': report_data
        })


#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::RMPLIR LE BILAN RADIOLOGIQUE ET L AFFICHER:::::::::::::::::::::::::::::

@method_decorator(csrf_exempt, name='dispatch')
class FillRadiologyReportView(View):
    def get_radiologist_from_token(self, request):
        """
        Extraire et vérifier le rôle de l'utilisateur à partir du token d'autorisation.
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # On suppose un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get('user_id')
            role = decoded.get('role')

            if not user_id:
                return None, JsonResponse({"error": "User ID not found in token"}, status=401)

            if role != 'Radiologist':
                return None, JsonResponse({"error": "Unauthorized role, not a radiologist"}, status=403)

            radiologist = get_object_or_404(Radiologist, id=user_id)
            return radiologist, None
        
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def post(self, request, assessment_id):
        # Vérifier si l'utilisateur est un radiologue
        radiologist, error_response = self.get_radiologist_from_token(request)
        if error_response:
            return error_response

        # Récupérer l'évaluation radiologique par ID
        assessment = get_object_or_404(RadiologyAssessment, id=assessment_id)

        # Vérifier si un rapport radiologique est déjà associé à cette évaluation
        if not assessment.radiology_report:
            return JsonResponse({"error": "No radiology report associated with this assessment"}, status=400)

        # Récupérer le rapport radiologique existant
        radiology_report = assessment.radiology_report

        # Extraire les données envoyées pour remplir le rapport
        date_of_image = request.POST.get('date_of_image')
        description = request.POST.get('description')
        image_data = request.FILES.get('image_data')  # Fichier image envoyé via 'FILES'

        # Validation des champs requis
        if not all([date_of_image, description, image_data]):
            return JsonResponse({"error": "Missing required fields: date_of_image, description, or image_data"}, status=400)

        # Mettre à jour le rapport radiologique existant
        radiology_report.date = date_of_image
        radiology_report.description = description
        radiology_report.radiologist = radiologist  # Le radiologue remplissant le rapport

        # Sauvegarder l'image dans le champ 'imageData'
        radiology_report.imageData = image_data  # L'image est enregistrée via 'FILES'
        
        # Sauvegarder les modifications
        radiology_report.save()

        return JsonResponse({
            'message': 'Radiology report updated successfully',
            'report_id': radiology_report.id
        })
import base64
from io import BytesIO
from PIL import Image

@method_decorator(csrf_exempt, name='dispatch')
class DisplayRadiologyReportView(View):
    def get_user_from_token(self, request):
        """
        Extraire l'ID de l'utilisateur à partir du token d'autorisation sans contrainte de rôle.
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            token = token.split(" ")[1]  # On suppose un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded.get('user_id')

            if not user_id:
                return None, JsonResponse({"error": "User ID not found in token"}, status=401)

            return user_id, None
        
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def image_to_base64(self, image):
        """
        Convertir l'image en base64 pour l'inclure dans la réponse.
        """
        if not image:
            return None
        image_file = BytesIO()
        img = Image.open(image)
        img.save(image_file, format='PNG')  # Ou le format de votre image
        image_file.seek(0)
        return base64.b64encode(image_file.read()).decode('utf-8')

    def get(self, request, assessment_id):
        # Vérifier l'utilisateur via le token (sans contrainte de rôle)
        user_id , error_response = self.get_user_from_token(request)
        if error_response:
            return error_response

        # Récupérer l'évaluation radiologique par ID
        assessment = get_object_or_404(RadiologyAssessment, id=assessment_id)

        # Vérifier si un rapport radiologique est associé à cette évaluation
        if not assessment.radiology_report:
            return JsonResponse({"error": "No radiology report associated with this assessment"}, status=400)

        # Récupérer le rapport radiologique existant
        radiology_report = assessment.radiology_report

        # Convertir l'image en base64 si elle existe
        image_data = self.image_to_base64(radiology_report.imageData) if radiology_report.imageData else None

        # Retourner les informations du rapport radiologique
        return JsonResponse({
            "report_id": radiology_report.id,
            "date_of_image": radiology_report.date,
            "description": radiology_report.description,
            "image_data": image_data,  # Ou vous pouvez renvoyer l'URL de l'image ici si vous ne souhaitez pas envoyer du base64
            "radiologist": radiology_report.radiologist.name,  # Exemple pour ajouter le nom du radiologue
        })







#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import jwt
from django.conf import settings
from api.models import EHR, Prescription, MedicalTreatment, Medecine, Doctor, Patient
from django.shortcuts import get_object_or_404
from django.db import transaction
import re
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(csrf_exempt, name='dispatch')
class CreatePrescriptionView(View):
    def post(self, request, *args, **kwargs):
        # Ensure the method is POST
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        # Get JWT from headers
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authorization token is missing"}, status=401)

        token = token.split(" ")[1]  # Assuming Bearer Token

        try:
            # Decode JWT
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()  # Normalize role

            # Validate role
            valid_roles = ['doctor']
            if role not in valid_roles:
                return JsonResponse({"error": "Unauthorized role"}, status=403)


            # If role is doctor, fetch doctor
            if role == 'doctor':
              doctor = get_object_or_404(Doctor, id=decoded.get('user_id'))                
              print(f"Doctor: {doctor}")

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # Parse request body
        try:
            data = json.loads(request.body)
            ehr_id = data.get("ehr_id")
            treatments = data.get("treatments", [])

            # Validate EHR ID
            ehr = EHR.objects.get(id=ehr_id)

            # Ensure EHR is linked to a patient
            patient = Patient.objects.get(ehr=ehr)

        except ObjectDoesNotExist: 
            return JsonResponse({"error": "EHR or Patient not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Create prescription
        try:
            prescription = Prescription.objects.create(
                isValid=False,
                doctor=doctor,
                ehr=ehr
            )

            # Create MedicalTreatment records
            for treatment in treatments:
                medicine_name = treatment.get("medicine")
                dose = treatment.get("dose")
                duration = treatment.get("duration")

                # Validate inputs
                if not medicine_name or dose is None or duration is None:
                    return JsonResponse({"error": "Missing treatment details"}, status=400)

                # Fetch or create medicine
                medicine, created = Medecine.objects.get_or_create(name=medicine_name)

                # Create MedicalTreatment
                MedicalTreatment.objects.create(
                    dose=dose,
                    Duration=duration,
                    medicine=medicine,
                    prescription=prescription
                )

            # Return success response
            return JsonResponse({
                "message": "Prescription created successfully",
                "prescription_id": prescription.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Invalid request method"}, status=405)
 