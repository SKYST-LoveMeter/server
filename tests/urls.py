from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path("", views.StartTestAPIView.as_view(), name="start_test"), 
    path("<int:test_id>/calendar", views.CalendarAPIView.as_view()),
    path("<int:test_id>/result", views.TestResultAPIView.as_view(), name="test_result"),
    path("<int:test_id>/result_view", views.TestResultViewAPIView.as_view()),
    path("<int:test_id>/result_detail/<int:love_id>", views.TestResultDetailAPIView.as_view()),
    path("love_category/", views.LoveCategoryCreate.as_view())
] 
