import jwt
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from api.models import BiologyReport, EHR
import json
import matplotlib.pyplot as plt
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_trend_graph(request):
    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)

    try:
        token = token.split(" ")[1]  # Assuming Bearer Token

        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Validate role
        if role != "labtechnician":
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Ensure the method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get data from request body (JSON)
    try:
        body = json.loads(request.body)
        ehr_id = body.get('ehr_id')  # Expecting 'ehr_id' in the JSON body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not ehr_id:
        return JsonResponse({'error': 'ehr_id is required'}, status=400)

    # Retrieve the EHR using ehr_id
    ehr = get_object_or_404(EHR, id=ehr_id)

    # Get all biological reports associated with the EHR where bloodSugarLevel is not null
    biological_reports = BiologyReport.objects.filter(ehr=ehr, bloodSugarLevel__isnull=False)

    # If no reports found
    if not biological_reports:
        return JsonResponse({"error": "No biological reports with blood sugar levels found."}, status=404)

    # Prepare data for graph: dates and corresponding blood sugar levels
    dates = []
    blood_sugar_levels = []

    for report in biological_reports:
        dates.append(report.date)
        blood_sugar_levels.append(report.bloodSugarLevel)

    # Sort by date (if necessary)
    sorted_dates, sorted_blood_sugar_levels = zip(*sorted(zip(dates, blood_sugar_levels)))

    # Create a plot for blood sugar level over time
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sorted_blood_sugar_levels, marker='o', color='b', linestyle='-', label='Blood Sugar Level')
    plt.xlabel('Date')
    plt.ylabel('Blood Sugar Level')
    plt.title('Blood Sugar Level Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Create an HTTP response with the image content
    response = HttpResponse(img_buf, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="blood_sugar_trend.png"'
    
    return response


@csrf_exempt
def generate_blood_pressure_trend(request):
    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)

    try:
        token = token.split(" ")[1]  # Assuming Bearer Token

        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Validate role
        if role != "labtechnician":
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Ensure the method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get data from request body (JSON)
    try:
        body = json.loads(request.body)
        ehr_id = body.get('ehr_id')  # Expecting 'ehr_id' in the JSON body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not ehr_id:
        return JsonResponse({'error': 'ehr_id is required'}, status=400)

    # Retrieve the EHR using ehr_id
    ehr = get_object_or_404(EHR, id=ehr_id)

    # Get all biological reports associated with the EHR where bloodPressure is not null
    biological_reports = BiologyReport.objects.filter(ehr=ehr, bloodPressure__isnull=False)

    # If no reports found
    if not biological_reports:
        return JsonResponse({"error": "No biological reports with blood pressure levels found."}, status=404)

    # Prepare data for graph: dates and corresponding blood pressure levels
    dates = []
    blood_pressure_levels = []

    for report in biological_reports:
        dates.append(report.date)
        blood_pressure_levels.append(report.bloodPressure)

    # Sort by date (if necessary)
    sorted_dates, sorted_blood_pressure_levels = zip(*sorted(zip(dates, blood_pressure_levels)))

    # Create a plot for blood pressure over time
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sorted_blood_pressure_levels, marker='o', color='g', linestyle='-', label='Blood Pressure')
    plt.xlabel('Date')
    plt.ylabel('Blood Pressure')
    plt.title('Blood Pressure Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Create an HTTP response with the image content
    response = HttpResponse(img_buf, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="blood_pressure_trend.png"'
    
    return response


@csrf_exempt
def generate_cholesterol_level_trend(request):
    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)

    try:
        token = token.split(" ")[1]  # Assuming Bearer Token

        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Validate role
        if role != "labtechnician":
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Ensure the method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get data from request body (JSON)
    try:
        body = json.loads(request.body)
        ehr_id = body.get('ehr_id')  # Expecting 'ehr_id' in the JSON body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not ehr_id:
        return JsonResponse({'error': 'ehr_id is required'}, status=400)

    # Retrieve the EHR using ehr_id
    ehr = get_object_or_404(EHR, id=ehr_id)

    # Get all biological reports associated with the EHR where cholesterolLevel is not null
    biological_reports = BiologyReport.objects.filter(ehr=ehr, cholesterolLevel__isnull=False)

    # If no reports found
    if not biological_reports:
        return JsonResponse({"error": "No biological reports with cholesterol levels found."}, status=404)

    # Prepare data for graph: dates and corresponding cholesterol levels
    dates = []
    cholesterol_levels = []

    for report in biological_reports:
        dates.append(report.date)
        cholesterol_levels.append(report.cholesterolLevel)

    # Sort by date (if necessary)
    sorted_dates, sorted_cholesterol_levels = zip(*sorted(zip(dates, cholesterol_levels)))

    # Create a plot for cholesterol level over time
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sorted_cholesterol_levels, marker='o', color='r', linestyle='-', label='Cholesterol Level')
    plt.xlabel('Date')
    plt.ylabel('Cholesterol Level')
    plt.title('Cholesterol Level Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Create an HTTP response with the image content
    response = HttpResponse(img_buf, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="cholesterol_level_trend.png"'
    
    return response




@csrf_exempt
def generate_blood_sugar_trend(request):
    # Get JWT from headers
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)

    try:
        token = token.split(" ")[1]  # Assuming Bearer Token

        # Decode JWT
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()  # Normalize role

        # Validate role
        if role != "labtechnician":
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Ensure the method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Get data from request body (JSON)
    try:
        body = json.loads(request.body)
        ehr_id = body.get('ehr_id')  # Expecting 'ehr_id' in the JSON body
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not ehr_id:
        return JsonResponse({'error': 'ehr_id is required'}, status=400)

    # Retrieve the EHR using ehr_id
    ehr = get_object_or_404(EHR, id=ehr_id)

    # Get all biological reports associated with the EHR where completeBloodCount is not null
    biological_reports = BiologyReport.objects.filter(ehr=ehr, completeBloodCount__isnull=False)

    # If no reports found
    if not biological_reports:
        return JsonResponse({"error": "No biological reports with complete blood count found."}, status=404)

    # Prepare data for graph: dates and corresponding complete blood count
    dates = []
    complete_blood_counts = []

    for report in biological_reports:
        dates.append(report.date)
        complete_blood_counts.append(report.completeBloodCount)

    # Sort by date (if necessary)
    sorted_dates, sorted_complete_blood_counts = zip(*sorted(zip(dates, complete_blood_counts)))

    # Create a plot for complete blood count over time
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sorted_complete_blood_counts, marker='o', color='m', linestyle='-', label='Complete Blood Count')
    plt.xlabel('Date')
    plt.ylabel('Complete Blood Count')
    plt.title('Complete Blood Count Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Create an HTTP response with the image content
    response = HttpResponse(img_buf, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="complete_blood_count_trend.png"'
    
    return response




@csrf_exempt
def generate_complete_blood_count_trend(request):
    # Authentification JWT
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Authorization token is missing"}, status=401)

    try:
        token = token.split(" ")[1]  # Supposons un Bearer Token
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        role = decoded.get("role", "").strip().lower()

        if role != "labtechnician":
            return JsonResponse({"error": "Unauthorized role"}, status=403)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)

    # Validation de la méthode
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Récupération des données JSON
    try:
        body = json.loads(request.body)
        ehr_id = body.get('ehr_id')
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    if not ehr_id:
        return JsonResponse({'error': 'ehr_id is required'}, status=400)

    # Recherche des rapports biologiques
    ehr = get_object_or_404(EHR, id=ehr_id)
    reports = BiologyReport.objects.filter(ehr=ehr, completeBloodCount__isnull=False)

    if not reports:
        return JsonResponse({"error": "No records found."}, status=404)

    # Extraction des données
    dates = []
    blood_counts = []

    for report in reports:
        dates.append(report.date)  # Date précise dans la DB
        blood_counts.append(report.completeBloodCount)

    # Tri par date
    sorted_dates, sorted_counts = zip(*sorted(zip(dates, blood_counts)))

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, sorted_counts, marker='o', color='g', linestyle='-', label='Complete Blood Count')
    plt.xlabel('Date')
    plt.ylabel('Complete Blood Count')
    plt.title('Complete Blood Count Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Enregistrement et envoi de l'image
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    response = HttpResponse(img_buf, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="complete_blood_count_trend.png"'
    
    return response