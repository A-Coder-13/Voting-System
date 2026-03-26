from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ext_User(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    gender = models.CharField(max_length=10)
    profession= models.CharField(max_length=100)

class PasswordOTP(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at= models.DateTimeField(auto_now_add=True)