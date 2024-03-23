from django.contrib import admin
from django.apps import apps
from .models import *

app = apps.get_app_config('tests')

# 모든 모델을 반복하여 admin 사이트에 등록
for model_name, model in app.models.items():
    admin.site.register(model)

# Register your models here.
