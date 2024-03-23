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
        # print(category)
        # Love.objects.create(name=category)
        queryset = LoveCategory.objects.all()
        # print(queryset)
        serializer = LoveCategorySerializer(queryset, many=True)
        data = {item['id']: item['name'] for item in serializer.data}
        test = Test.objects.create(user= request.user)
        context = {
            "category" : data,
            "test_id" : test.id
        }
        return Response(context)

class CalendarAPIView(APIView):
    def get (self, request):
        tests= Test.objects.filter(user = request.user)
        serialized_tests =TestSerializer(tests,many=True)
        context = [
            { "created_at" : test["created_at"],
              "test_id" : test["id"]
        }
            for test in serialized_tests.data
        ]
        return Response(context) 

class AnalysisAPIView(APIView):
    def post (self, request,test_id):
        test = Test.objects.get(id=test_id)

        highest_prediction = test.loves.all().order_by('-prediction').first()
        highest_value = test.loves.all().order_by('-value').first()

        difference_list = []
        love_id_list = []

        loves = test.loves.all()
        for love in loves : 
            difference = love.result - love.prediction
            difference_list.append(difference)
            love_id_list.append(love.id)
        
        max_value = max(difference_list)  # 배열에서 최대값을 찾음
        max_index = difference_list.index(max_value)    

        min_value = min(difference_list)
        min_index = difference_list.index(min_value)

        over_value = love.objects.get(id = love_id_list[max_index]).name.name
        under_value = love.objects.get(id = love_id_list[min_index]).name.name

        recommendation = get_completion(test_id, under_value)        
        
        context = {
            "highest_prediction" : highest_prediction,
            "highest_value" : highest_value,
            "over_value" : over_value,
            "under_value" : under_value,
            "recommendation" : recommendation
        }
        return Response(context) 

class TestResultAPIView(APIView):
    def post (self, request, test_id):
        received_data = request.data
        # print(request.data)
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
                {"name": LoveCategory.objects.get(id=item['name']).name, 
                "percentage": item['result'],
                "love_id" : item['id']
                }
                for item in serializer.data 
            ]

        return Response(context)    

class TestResultViewAPIView(APIView):
    def post (self, request, test_id):
        test = Test.objects.get(id= test_id)
        serializer = LoveSerializer(test.loves.all(), many=True)
        
        context = [
                {"name": LoveCategory.objects.get(id=item['name']).name, 
                "percentage": item['result'],
                "love_id" : item['id']
                }
                for item in serializer.data 
            ]  
        
        return Response(context) 

class TestResultDetailAPIView(APIView):
    def post (self, request, test_id, love_id):
        test = Test.objects.get(id= test_id)
        love = Love.objects.get(id=love_id)

        efforts = love.efforts.all().filter(test=test) 
        serialized_efforts = EffortSerializer(efforts, many=True).data

        all_loves = test.loves.all().filter(id__lt=test_id)
        serialized_loves = LoveSerializer(all_loves, many=True).data

        context = {
            "efforts": [effort['description'] for effort in serialized_efforts],
            "previous_loves": [love['result'] for love in serialized_loves]
        }
        
        return Response(context)            

class LoveCategoryCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoveCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

import openai
from config.settings.deploy import OPEN_API_KEY
key = OPEN_API_KEY
openai.api_key=key
def get_completion(test_id, under_value):
    messages = [
        {"role": "system", "content": "나는 지금 서비스를 기획하고 있어. 이 서비스는 사랑하는 것들의 순위를 선정하고, 실제 그것들에 주는 애정을 비교하는 서비스야. 비교를 통해 사용자에게 적합한 조언을 해줘야돼."}
    ]
    # 많은 시간을 쏟는 일들을 나열
    test = Test.objects.get(id=test_id)
    efforts = list(Effort.objects.filter(test=test, value=3))
    context = ", ".join(str(e) for e in efforts)
    messages.append({"role": "assistant", "content": f"{context}를 자주하는 사람"})
    messages.append({"role": "user", "content": f"{under_value}게 애정을 더 쏟기 위해서 할만한 행동을 한 문장으로 추천해줘"})
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response = query.choices[0].message["content"]
    return response