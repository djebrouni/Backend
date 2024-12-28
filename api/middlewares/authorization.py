from django.http import JsonResponse
from functools import wraps

def verify_role(*allowed_roles):
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            # Get role from request
            user_role = request.role
            
            # check if in allowed role
            if user_role not in [role.value for role in allowed_roles]:
                return JsonResponse({'error': 'Forbidden: Insufficient permissions'}, status=403)
            
            # Proceed to the view function if the role is allowed
            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
