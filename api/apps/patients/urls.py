from django.urls import path
from .views import create_patient_dpi
from .views import consultation_dpi ,UpdateProfileView,ProfileView

urlpatterns = [
    path('create_patient_dpi/', create_patient_dpi, name='create_patient_dpi'),
   path('profile/', ProfileView.as_view(), name='profile'),
   path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('consultation-dpi/', consultation_dpi, name='consultation_dpi'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('profile/', ProfileView.as_view(), name='profile'),


]
