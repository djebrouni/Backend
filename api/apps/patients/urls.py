from django.urls import path
from .views import create_patient_dpi
from .views import consultation_dpi

urlpatterns = [
    path('create_patient_dpi/', create_patient_dpi, name='create_patient_dpi'),
   
    path('consultation-dpi/', consultation_dpi, name='consultation_dpi'),

]
