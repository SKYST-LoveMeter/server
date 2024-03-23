from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view

@api_view(['GET'])
def start_test (request):
    categories = LoveCategory.objects.all()
    serialized_categories = LoveCategorySerializer(categories, many= True)
    context = {
        "categories" : serialized_categories    
    }
    return Response(context)    

