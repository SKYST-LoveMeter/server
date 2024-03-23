from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

@api_view(['GET'])
def start_test (request):
    categories = Category.objects.all()
    serialized_categories = CategorySerializer(categories, many= True)
    context = {
        "categories" : serialized_categories    
    }
    return Response(context)    

