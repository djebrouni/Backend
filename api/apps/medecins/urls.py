from django.urls import path
from .views import rechercheDpiParNss

urlpatterns = [
    path('search-patient/', rechercheDpiParNss, name='search_patient'),
]
