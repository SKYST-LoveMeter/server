from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView),
    path("signup/", views.SignUpAPIView.as_view()),
]