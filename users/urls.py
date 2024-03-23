from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view()),
    path("signup/", views.SignUpAPIView.as_view()),
    path("info/", views.UserInfoAPIView.as_view()),
]