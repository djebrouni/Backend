from django.urls import path
from .views import PatientSignupView
from .views import SignInView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', PatientSignupView.as_view(), name='signup'),
]
