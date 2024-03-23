from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path("", views.StartTestAPIView.as_view(), name="start_test"), 
    path("<int:test_id>/result", views.TestResultAPIView.as_view(), name="test_result"),
    path("love_category/", views.LoveCategoryCreate.as_view())
] 
