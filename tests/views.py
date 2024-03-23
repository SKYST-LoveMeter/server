from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

@api_view(['GET'])
def result (request):
    context = {
        
    }
    return Response(context)