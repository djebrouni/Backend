from django.urls import path, include

# include urls of apps
urlpatterns = [
    path('auth/', include('api.apps.auth.urls')),    
    path('auth/', include('api.apps.medecins.urls')),    
    path('auth/', include('api.apps.patients.urls')),    
    path('auth/', include('api.apps.users.urls')),    
]
