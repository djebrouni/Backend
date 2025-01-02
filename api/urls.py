from django.urls import path, include

# include urls of apps
urlpatterns = [
    path('', include('api.apps.users.urls')),    
    path('auth/', include('api.apps.auth.urls')),    
    path('medecins/', include('api.apps.medecins.urls')),    
    path('patients/', include('api.apps.patients.urls')),    
    path('infermier/', include('api.apps.infermier.urls')), 
    path('labtechnicians/', include('api.apps.labtechnicians.urls')), 
    path('get/', include('api.apps.get.urls')), 
    path('sgph/', include('api.apps.sgph.urls')),
]
