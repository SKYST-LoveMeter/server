from rest_framework import serializers #추가
from .models import *

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['created_at', 'updated_at', 'user', 'id']
    
class EffortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effort
        fields = '__all__'

class LoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Love
        fields = ['name', 'prediction', 'result']

class LoveCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoveCategory
        fields = '__all__'
    # def to_representation(self, instance):
    #     rep = super(LoveCategorySerializer, self).to_representation(instance)
    #     return {rep['id']: rep['name']}





#건강, 가족, 커리어, 자신, 친구, 연인, 부모님, 외모,