import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from api.helper.getModels import getModel

def verify_user(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
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
        user_id = decoded_data.get('user_id')
        user_role = decoded_data.get('role')
        
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
        request.role = user_role
        
        # Proceed to the view
        return view_func(self, request, *args, **kwargs)
    
    return wrapper

