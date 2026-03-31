from django.db import models
from django.contrib.auth.models import User
from questonaries.models import Question


# Create your models here.
class Comments(models.Model):
    text = models.TextField(null=False)
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Likes(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentsReply(models.Model):
    text = models.TextField(null=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
