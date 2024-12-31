from django.urls import path
from .views import CareProvidedCreateView, CareProvidedDetailView, CareProvidedUpdateView

urlpatterns = [
    path('careprovided/create/', CareProvidedCreateView.as_view(), name='careprovided_create'),
    path('careprovided/<int:care_provided_id>/', CareProvidedDetailView.as_view(), name='careprovided_detail'),
    path('careprovided/update/<int:care_provided_id>/', CareProvidedUpdateView.as_view(), name='careprovided_update'),  
]
