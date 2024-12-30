""""
import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from api.helper.getModels import getModel
#//
def verify_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Access Denied'}, status=401)

        # Extract the token
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return JsonResponse({'error': 'Access Denied'}, status=401)

        # Decode the token
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Expired Token'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid Token'}, status=401)

        # get data from token
        user_id = decoded_data.get('userId')
        user_role = decoded_data.get('userRole')
        
        # verify if user exist
        Model = getModel(user_role)
        if not Model:
            return JsonResponse({'error': 'Invalid Role'}, status=401)
        
        try:
            user = Model.objects.get(id=user_id)
        except Model.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Attach data to the request
        request.user = user
        request.Model = Model
        request.role = decoded_data.get('userRole')
        
        # Proceed to the view
        return view_func(request, *args, **kwargs)
    
    return wrapper
#
    """
import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from api.helper.getModels import getModel
#//

def verify_user(view_func):
    """
    Middleware to verify JWT token and authenticate the user based on role and ID.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Récupérer l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Accès refusé'}, status=401)

        # Extraire le token
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return JsonResponse({'error': 'Accès refusé'}, status=401)

        # Décoder le token
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expiré'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token invalide'}, status=401)

        # Récupérer les données du token
        user_id = decoded_data.get('userId')
        user_role = decoded_data.get('userRole')

        # Vérifier si le modèle utilisateur existe pour le rôle
        Model = getModel(user_role)
        if not Model:
            return JsonResponse({'error': 'Rôle invalide'}, status=401)

        try:
            # Récupérer l'utilisateur en fonction de l'ID et du modèle
            user = Model.objects.get(id=user_id)
        except Model.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

        # Attacher les données de l'utilisateur à la requête
        request.user = user
        request.Model = Model
        request.role = decoded_data.get('userRole')

        # Continuer avec la vue
        return view_func(request, *args, **kwargs)
    
    return wrapper
