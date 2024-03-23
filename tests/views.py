from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view

@api_view(['POST'])
def start_test (request):
    categories = LoveCategory.objects.all()
    serialized_categories = LoveCategorySerializer(categories, many= True)
    context = {
        "categories" : serialized_categories    
    }
    return Response(context)    

@api_view(['POST'])
def test_result (request, test_id):
    received_data = request.data
    loves = received_data['love']
    efforts = received_data['effort']

    for effort in efforts :
        Effort.objects.create(description= effort['description'], test_id = test_id) 
    
    for love in loves :
        made_love = Love.objects.create(name = love['name'], prediction = love['percentage'])

        made_love.efforts.add(related_effort) 




    context = {
       
    }
    return Response(context)    



