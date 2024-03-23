from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path("", views.start_test, name="start_test"), 
] 
