from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=200) 

class Question(models.Model):
    ques = models.TextField(null=False)
    q_desc = models.TextField(null=True)
    expiry = models.DateTimeField()
    hashtags = models.TextField(null=True)
    img = models.ImageField(
        upload_to='images/Ques_Covers/%Y/%m/%d/',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg','jpeg','png','webp', 'gif'],
            message="Only this image formates are allowed: jpg, jpeg, gif, png, webp.")],
          blank=True, null=True
        )
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cat_id = models.ForeignKey(Category,on_delete=models.PROTECT)
    created_at= models.DateTimeField(auto_now_add=True)


class options(models.Model):
    option = models.TextField(null=False)
    o_desc = models.TextField(null=True)
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)


class Vote_Click(models.Model):
    opt_id = models.ForeignKey(options,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)


