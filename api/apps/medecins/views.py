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
from api.models import Patient, EHR, RadiologyAssessment, Consultation, Diagnostic, BiologicalAssessment, BiologyReport, LabTechnician, Doctor
from django.contrib.auth.models import User



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


import jwt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.models import BiologicalAssessment, Doctor
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

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

        # Créer l'évaluation biologique et l'associer au médecin et au patient via l'EHR
        biological_assessment = BiologicalAssessment.objects.create(
            date=datetime.now().strftime("%Y-%m-%d"),
            patient_name=patient_name,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            tests_to_conduct=tests_to_conduct,
            ehr=ehr,
            doctor=doctor  # Associer l'évaluation biologique au médecin
        )

        return JsonResponse({
            'message': 'Biological assessment created successfully',
            'assessment_id': biological_assessment.id
        })


#:::::::::::::::::::::::::::::::::::::::::::CREATION RADIOLOGY ASSESMEENT ET SON DISPLAY::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@method_decorator(csrf_exempt, name='dispatch')
class CreateRadiologyAssessmentView(View):
    def get_doctor_from_token(self, request):
        # Extraire le token de la requête
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)

        try:
            # Extraire le token Bearer
            token = token.split(" ")[1]  # On suppose que le token est de type 'Bearer <token>'
            
            # Décoder le token pour obtenir l'user_id et le rôle
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Récupérer l'ID de l'utilisateur et le rôle du token
            user_id = decoded.get('user_id')
            role = decoded.get('role')

            if not user_id:
                return None, JsonResponse({"error": "User ID not found in token"}, status=401)
            
            # Si le rôle est 'doctor', alors tu récupères le médecin
            if role != 'doctor':
                return None, JsonResponse({"error": "Unauthorized role, not a doctor"}, status=403)

            # Trouver le médecin associé à cet user_id
            doctor = get_object_or_404(Doctor, id=user_id)  # Utilise 'id' pour trouver le médecin

            return doctor, None
        
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def post(self, request, ehr_id):
        # Vérifier et récupérer le médecin à partir du token
        doctor, error_response = self.get_doctor_from_token(request)
        if error_response:
            return error_response

        # Récupérer l'EHR du patient
        ehr = get_object_or_404(EHR, id=ehr_id)

        # Extraire les informations du patient depuis l'EHR
        patient = ehr.patient
        patient_name = f"{patient.name} {patient.surname}"
        date_of_birth = patient.dateOfBirth.strftime("%Y-%m-%d")
        gender = patient.gender
        age = self.calculate_age(patient.dateOfBirth)

        # Récupérer les données JSON envoyées pour l'évaluation radiologique
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Extraire le type d'imagerie
        imaging_type = data.get('imaging_type')

        # Validation des champs requis
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
            doctor=doctor  # Lier le médecin à l'évaluation radiologique
        )

        return JsonResponse({
            'message': 'Radiology assessment created successfully',
            'assessment_id': radiology_assessment.id
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
            response_data.append({
                "id": assessment.id,
                "date": assessment.date.strftime("%Y-%m-%d"),
                "patient_name": assessment.patient_name,
                "date_of_birth": assessment.date_of_birth.strftime("%Y-%m-%d"),
                "age": assessment.age,
                "gender": assessment.gender,
                "imaging_type": assessment.imaging_type,
                "doctor_name": f"{assessment.doctor.name} {assessment.doctor.surname}" if assessment.doctor else "Unknown Doctor",
            })

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
            token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()  # Extraire et comparer le rôle en minuscules
            return role, None
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def post(self, request, ehr_id):
        # Vérifier le rôle de l'utilisateur
        role, error_response = self.get_user_role_from_token(request)
        if error_response:
            return error_response

        print(f"User role extracted from token: {role}")  # Ligne de débogage

        if role != "labtechnician":
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        # Récupérer les données JSON envoyées
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

        # Vérifier l'existence du Dossier Médical Électronique (EHR)
        ehr = get_object_or_404(EHR, id=ehr_id)

        # Récupérer le médecin directement via le champ 'creator' de l'EHR
        doctor = ehr.creator  # Le médecin qui a créé l'EHR

        if not doctor:
            return JsonResponse({"error": "No doctor associated with this EHR"}, status=400)

        # Récupérer le technicien de laboratoire à partir du token ou du contexte
        lab_technician = LabTechnician.objects.first()  # Vous pouvez aussi chercher par l'utilisateur connecté si nécessaire

        # Créer un nouveau rapport biologique lié à l'EHR
        report = BiologyReport.objects.create(
            bloodSugarLevel=blood_sugar_level,
            bloodPressure=blood_pressure,
            cholesterolLevel=cholesterol_level,
            completeBloodCount=complete_blood_count,
            doctor=doctor,  # Le médecin extrait directement du champ 'creator' de l'EHR
            lab_technician=lab_technician,  # Assurez-vous que le technicien est lié
            ehr=ehr  # Lier le rapport à l'EHR du patient
        )

        return JsonResponse({
            'message': 'Biology report created successfully',
            'report_id': report.id
        })


@method_decorator(csrf_exempt, name='dispatch')
class DisplayBiologyReportsView(View):
    def get_user_role_from_token(self, request):
        """
        Extrait le rôle de l'utilisateur à partir du token d'autorisation.
        """
        token = request.headers.get("Authorization")
        if not token:
            return None, JsonResponse({"error": "Authorization token is missing"}, status=401)
        try:
            token = token.split(" ")[1]  # En supposant que le token est un Bearer Token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded.get("role", "").strip().lower()  # Extraire et comparer le rôle en minuscules
            return role, None
        except jwt.ExpiredSignatureError:
            return None, JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return None, JsonResponse({"error": "Invalid token"}, status=401)

    def get(self, request, ehr_id):
        # Vérifier le rôle de l'utilisateur
        role, error_response = self.get_user_role_from_token(request)
        if error_response:
            return error_response

        if role not in ["labtechnician", "doctor"]:  # Vous pouvez ajuster en fonction des rôles autorisés
            return JsonResponse({"error": "You are not authorized to perform this action"}, status=403)

        # Récupérer l'EHR avec l'ID
        ehr = get_object_or_404(EHR, id=ehr_id)

        # Récupérer tous les rapports biologiques associés à cet EHR
        reports = BiologyReport.objects.filter(ehr=ehr)

        if not reports.exists():
            return JsonResponse({"error": "No biology reports found for this EHR"}, status=404)

        # Format des données à afficher
        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'bloodSugarLevel': report.bloodSugarLevel,
                'bloodPressure': report.bloodPressure,
                'cholesterolLevel': report.cholesterolLevel,
                'completeBloodCount': report.completeBloodCount,
                'doctor': report.doctor.name if report.doctor else None,
                'labTechnician': report.lab_technician.name if report.lab_technician else None,
            })

        return JsonResponse({
            'message': 'Biology reports retrieved successfully',
            'reports': reports_data
        })
