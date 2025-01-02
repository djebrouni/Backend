from django.urls import path
from .views import HospitalRecordsView, DoctorRecordsView
from .views import PrescriptionDetailView, CareProvidedDetailView


urlpatterns = [
    path('hospital-records/', HospitalRecordsView.as_view(), name='hospital-records'),
    path('doctor-records/', DoctorRecordsView.as_view(), name='doctor-records'),
    path('prescription/<int:prescription_id>/', PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('careprovided/<int:care_id>/', CareProvidedDetailView.as_view(), name='care_provided_detail'),
]

