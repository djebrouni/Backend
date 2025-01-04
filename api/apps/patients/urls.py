from django.urls import path
from .views import create_patient_dpi
from .views import UpdateProfileView,ProfileView, PatientInfoView,CareProvidedView,PrescriptionView,PatientPrescriptionsView

urlpatterns = [
    path('create_patient_dpi/', create_patient_dpi, name='create_patient_dpi'),
   path('profile/', ProfileView.as_view(), name='profile'),
   path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
   # path('consultation-dpi/', consultation_dpi, name='consultation_dpi'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('patient-info/<str:nss>/', PatientInfoView.as_view(), name='get_patient_info'),
    path('patient/<str:nss>/care/', CareProvidedView.as_view(), name='get_care'),
    path('patient/prescription/<int:prescription_id>/', PrescriptionView.as_view(), name='get_prescriptions'),
    path('patient/prescriptions/<str:nss>/',PatientPrescriptionsView.as_view(), name='get_patient_info'),

]

