


from .views import CreatePrescriptionView, DisplayRadiologyReportView, FillRadiologyReportView, rechercheDpiParNss
from django.urls import path
from .views import ConsultationCreateView, ConsultationUpdateView ,ConsultationSummaryView,CreateBiologicalAssessmentView,DisplayBiologicalAssessmentView,DisplayRadiologyAssessmentView,CreateRadiologyAssessmentView,FillBiologyReportView,DisplayBiologyReportsView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      path('search-patient/', rechercheDpiParNss, name='search_patient'),
      #creation et mise ajour de consultation
    path('consultation/create/', ConsultationCreateView.as_view(), name='consultation_create'),
   path('consultation/update/<int:consultation_id>/', ConsultationUpdateView.as_view(), name='consultation_update'),
   #affichage du summary
   path('consultation/summary/<int:consultation_id>/', ConsultationSummaryView.as_view(), name='consultation_summary'),
   #creation du bilan biologique
   path('create_biological_assessment/<int:ehr_id>/', CreateBiologicalAssessmentView.as_view(), name='create_biological_assessment'),
   path('view_biological_assessment/<int:ehr_id>/', DisplayBiologicalAssessmentView.as_view(), name='view_biological_assessment'),
   #remplisssage des resultats et affichage des resultats biio
   path('biological_assessment/fill_report/<int:assessment_id>/', FillBiologyReportView.as_view(), name='fill_biology_report'),
   path('biological_assessment/display_report/<int:assessment_id>/', DisplayBiologyReportsView.as_view(), name='display_biology_report'),
   #creation bilan radiolo
   path('create_radiology_assessment/<int:ehr_id>/', CreateRadiologyAssessmentView.as_view(), name='create_radiology_assessment'),
   path('display_radiology_assessment/<int:ehr_id>/', DisplayRadiologyAssessmentView.as_view(), name='display_radiology_assessment'),
   #remplisssage des resultats et affichage des resultats radio
    path('display-radiology-report/<int:assessment_id>/', DisplayRadiologyReportView.as_view(), name='display_radiology_report'),
    path('fill-radiology-report/<int:assessment_id>/', FillRadiologyReportView.as_view(), name='fill_radiology_report'),
    #creation prescription
     path('prescriptions/create/', CreatePrescriptionView.as_view(), name='create_prescription'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
