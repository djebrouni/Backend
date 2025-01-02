from django.urls import path
from .views import PatientSignupView
from .views import SignInView
from .views import UpdateProfileView,ProfileView
urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', PatientSignupView.as_view(), name='signup'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('profile/', ProfileView.as_view(), name='profile'),


]
