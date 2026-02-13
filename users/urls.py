from django.urls import path
from .views import RegisterView, LoginView, ConfirmView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("confirm/", ConfirmView.as_view()),
]


