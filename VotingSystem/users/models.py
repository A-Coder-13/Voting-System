from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class Ext_User(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    gender = models.CharField(max_length=10)
    profession= models.CharField(max_length=100)

class PasswordOTP(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at= models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='profile')
    profile_picture = models.ImageField(
        upload_to='images/profile_pictures/%Y/%m/%d/',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg','jpeg','png','webp', 'gif'],
            message="Only this image formates are allowed: jpg, jpeg, gif, png, webp.")],
          blank=True, null=True
        )
    bio = models.TextField(blank=True, max_length=300)
    location = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.username