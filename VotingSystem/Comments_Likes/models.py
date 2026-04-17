from django.db import models
from django.contrib.auth.models import User
from questonaries.models import Question


# Create your models here.
class Comments(models.Model):
    text = models.TextField(null=False)
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class PostLikes(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
class CommentsLikes(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    c_id = models.ForeignKey(Comments,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentsReply(models.Model):
    text = models.TextField(null=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




class Folowers(models.Model):
    user_folow = models.ForeignKey(User,on_delete=models.CASCADE,related_name="uer_folow") 
    folower = models.ForeignKey(User,on_delete=models.CASCADE) 
    created_At =models.DateTimeField(auto_now_add=True)