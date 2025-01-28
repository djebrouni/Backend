from django.urls import path
from .views import PatientInfoView,CareProvidedView,PrescriptionView,PatientPrescriptionsView, DPIView


urlpatterns = [
    path('dpi/', DPIView.as_view(), name='create_patient_dpi'),
    # path('consultation-dpi/', consultation_dpi, name='consultation_dpi'),
    path('patient-info/<str:nss>/', PatientInfoView.as_view(), name='get_patient_info'),
    path('patient/<str:nss>/care/', CareProvidedView.as_view(), name='get_care'),
    path('patient/prescription/<int:prescription_id>/', PrescriptionView.as_view(), name='get_prescriptions'),
    path('patient/prescriptions/<str:nss>/',PatientPrescriptionsView.as_view(), name='get_patient_info'),
    
]
