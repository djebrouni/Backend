from django.urls import path
from .views import SignUpView
from .views import SignInView

urlpatterns = [
    path('signin', SignInView.as_view(), name='signin'),
    path('signup', SignUpView.as_view(), name='signup'),
]
