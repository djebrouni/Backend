from django.urls import path
from .views import UserProfileView
urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='get_user_profile'),
]