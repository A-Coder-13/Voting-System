from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=200) 

class Question(models.Model):
    ques = models.TextField(null=False)
    q_desc = models.TextField(null=True)
    expiry = models.DateField()
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)


class options(models.Model):
    option = models.TextField(null=False)
    o_desc = models.TextField(null=True)
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)


