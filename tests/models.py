from django.db import models
from users.models import User

# Create your models here.
class Test(models.Model) :
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  loves = models.ManyToManyField('Love')

class Effort(models.Model) :
  description = models.CharField(max_length=1000, null= False)
  test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Love(models.Model) : 
  name = models.CharField(max_length=1000, null= False)
  prediction = models.PositiveIntegerField(default=0)
  result = models.PositiveIntegerField(default=0)
  efforts = models.ManyToManyField(Effort)

class LoveCategory(models.Model) :
  name = models.CharField(max_length=1000, null= False)
