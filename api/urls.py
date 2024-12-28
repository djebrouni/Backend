from django.urls import path
from .views import PatientSignupView
from .views import SignInView

urlpatterns = [
    path('signup/', PatientSignupView.as_view(), name='signup'),  # Define the signup endpoint
        path('signin/', SignInView.as_view(), name='signin'),

]
