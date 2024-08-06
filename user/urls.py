from django.urls import path
from .views import RegisterView, LoginView, CurrentUserView

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/current/', CurrentUserView.as_view(), name='current_user'),
]
