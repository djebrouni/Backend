from django.urls import path
from .views import UpdateProfileView,ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    
]
