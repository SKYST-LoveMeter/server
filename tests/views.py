from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import *

class StartTestAPIView(APIView):
    def get (self,request):
        category= LoveCategory.objects.get(id=1)
        print(category)
        Love.objects.create(name=category)
        queryset = LoveCategory.objects.all()
        print(queryset)
        serializer = LoveCategorySerializer(queryset, many=True)
        data = {item['id']: item['name'] for item in serializer.data}
        test = Test.objects.create(user= request.user)
        context = {
            "category" : data,
            "test_id" : test.id
        }
        return Response(context)
   

class TestResultAPIView(APIView):
    def get (self, request, test_id):
        queryset = Test.objects.get(id=test_id)

        if not queryset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

        love_list = queryset.loves.all()
        serializer = LoveSerializer(love_list, many=True)

        # test가 가지고 있는 loves에 대해서, 각각의 name과 result를 가져와서 저장.
        myList = []    

        for item in serializer.data:
            myList.append(
                {"name": LoveCategory.objects.get(id=item['name']).name, "percentage": item['result']}
            )

        return Response(myList)

    def post (self, request, test_id):
        received_data = request.data
        print(request.data)
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
                love_category = LoveCategory.objects.get(id=lover)
                love = Love.objects.get(name=love_category, id__gte=love_id_list[0])
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


class LoveCategoryCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoveCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CalendarAPIView(APIView):
    def get(self, request):
        user = request.user
        queryset = Test.objects.filter(user=user)
        serializer = TestSerializer(queryset, many=True)

        myList = []

        for item in serializer.data:
            myList.append({
                "id": item['id'],
                "created_at": item['created_at'],
                "updated_at": item['updated_at'],
            })
        
        return Response(myList)
    

