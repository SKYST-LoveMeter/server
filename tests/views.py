from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

@api_view(['Get'])
def start_test (request):
    queryset = LoveCategory.objects.all()
    serializer = LoveCategorySerializer(queryset, many=True)
    data = {item['id']: item['name'] for item in serializer.data}
    test = Test.objects.create(user= request.user)
    context = {
        "category" : data,
        "test_id" : test.id
    }
    return Response(context)
   

@api_view(['Post'])
def test_result (request, test_id):
    received_data = request.data
    loves = received_data['love']
    efforts = received_data['effort']

    made_test = Test.objects.get(id= test_id)

    love_id_list = []
    for love in loves :
        category = LoveCategory.objects.get(id=love['id'])
        made_love = Love.objects.create(name = category, prediction = love['percentage'])
        made_test.loves.add(made_love)
        love_id_list.append(made_love.id)
   
    total = 0
    for effort in efforts :
        made_effort = Effort.objects.create(description= effort['description'], test = made_test, value=effort['value']) 
        for lover in effort['lovers'] : 
            love = Love.objects.get(id = love_id_list[lover-1])
            love.efforts.add(made_effort)
        total = total + effort['value'] * len(effort['lovers'])

    for love_id in love_id_list :
        love = Love.objects.get(id = love_id)
        tmp = 0 
        for effort in love.efforts.all() :
            tmp = tmp + effort.value
        love.result = tmp/total * 100
        love.save()

    serializer = LoveSerializer(made_test.loves.all(), many=True)
    context = [
            {"name": LoveCategory.objects.get(id=item['name']).name, "percentage": item['result']}
            for item in serializer.data
        ]

    return Response(context)    

class LoveCategory(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoveCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)