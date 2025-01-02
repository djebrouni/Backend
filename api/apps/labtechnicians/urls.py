from django.urls import path
from . import views

urlpatterns = [
    path('generate_blood_sugar_trend/', views.generate_blood_sugar_trend, name='generate_blood_sugar_trend'),
    path('generate_blood_pressure_trend/', views.generate_blood_pressure_trend, name='generate_blood_pressure_trend'),
    path('generate_cholesterol_level_trend/', views.generate_cholesterol_level_trend, name='generate_cholesterol_level_trend'),
    path('generate_complete_blood_count_trend/', views.generate_complete_blood_count_trend, name='generate_complete_blood_count_trend'),
]
 