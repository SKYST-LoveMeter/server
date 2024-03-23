from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path("", views.start_test, name="start_test"), 
    path("<int:test_id>/result", views.test_result, name="test_result"),
    path("love_category/", views.LoveCategory.as_view())
] 
