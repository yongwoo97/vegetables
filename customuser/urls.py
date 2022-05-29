from django.urls import path
from .views import RegisterView, LoginView, UsernameUniqueView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('unique/', UsernameUniqueView.as_view()),
]
