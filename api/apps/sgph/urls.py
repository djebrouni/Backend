from django.urls import path
from .views import ValidatePrescriptionView ,PrescriptionListView
urlpatterns = [
    path('validate-prescription/', ValidatePrescriptionView.as_view(), name='validate-prescription'),
    path('list-prescriptions/', PrescriptionListView.as_view(), name='list-prescriptions'),

]
