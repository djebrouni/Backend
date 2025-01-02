


from .views import rechercheDpiParNss
from django.urls import path
from .views import ConsultationCreateView, ConsultationUpdateView ,ConsultationSummaryView,CreateBiologicalAssessmentView,DisplayBiologicalAssessmentView,DisplayRadiologyAssessmentView,CreateRadiologyAssessmentView,FillBiologyReportView,DisplayBiologyReportsView
from .views import CreatePrescriptionView ,ValidatePrescriptionView

urlpatterns = [
      path('search-patient/', rechercheDpiParNss, name='search_patient'),
    path('consultation/create/', ConsultationCreateView.as_view(), name='consultation_create'),
   path('consultation/update/<int:consultation_id>/', ConsultationUpdateView.as_view(), name='consultation_update'),
   path('consultation/summary/<int:consultation_id>/', ConsultationSummaryView.as_view(), name='consultation_summary'),
   path('create_biological_assessment/<int:ehr_id>/', CreateBiologicalAssessmentView.as_view(), name='create_biological_assessment'),
   path('view_biological_assessment/<int:ehr_id>/', DisplayBiologicalAssessmentView.as_view(), name='view_biological_assessment'),
   path('create_radiology_assessment/<int:ehr_id>/', CreateRadiologyAssessmentView.as_view(), name='create_radiology_assessment'),
   path('display_radiology_assessment/<int:ehr_id>/', DisplayRadiologyAssessmentView.as_view(), name='display_radiology_assessment'),
  path('create_biology_report/<int:ehr_id>/', FillBiologyReportView.as_view(), name='create_biology_report'),
   path('display_biology_reports/<int:ehr_id>/', DisplayBiologyReportsView.as_view(), name='display_biology_reports'),
   path('prescriptions/create/', CreatePrescriptionView.as_view(), name='create_prescription'),
   path('validate_prescription/', ValidatePrescriptionView.as_view(), name='validate_prescription'),

]
