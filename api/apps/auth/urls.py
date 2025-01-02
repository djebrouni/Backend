from django.urls import path
from .views import SignUpView
from .views import SignInView
from .views import UpdateProfileView,ProfileView
urlpatterns = [
    path('signin', SignInView.as_view(), name='signin'),
    path('signup', SignUpView.as_view(), name='signup'),
]
