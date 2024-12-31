from django.urls import path
from .views import rechercheDpiParNss
from django.urls import path
from .views import ConsultationCreateView, ConsultationUpdateView ,ConsultationSummaryView

urlpatterns = [
      path('search-patient/', rechercheDpiParNss, name='search_patient'),
    path('consultation/create/', ConsultationCreateView.as_view(), name='consultation_create'),
   path('consultation/update/<int:consultation_id>/', ConsultationUpdateView.as_view(), name='consultation_update'),
   path('consultation/summary/<int:consultation_id>/', ConsultationSummaryView.as_view(), name='consultation_summary'),
]
