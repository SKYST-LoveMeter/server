from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view

@api_view(['Get'])
def start_test (request):
    queryset = LoveCategory.objects.all()
    serializer = LoveCategorySerializer(queryset, many=True)
    data = {item['id']: item['name'] for item in serializer.data}
    return Response(data)
   

@api_view(['POST'])
def test_result (request, test_id):
    received_data = request.data
    loves = received_data['love']
    efforts = received_data['effort']

    for love in loves :
        Love.objects.create(name = love['name'], prediction = love['percentage'])

    for effort in efforts :
        made_effort = Effort.objects.create(description= effort['description'], test_id = test_id) 
        for lover in effort['lovers'] : 
            love = Love.objects.get(id = lover)
            love.efforts.add(made_effort)   
    context = {
       
    }
    return Response(context)    



