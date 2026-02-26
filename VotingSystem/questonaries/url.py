from django.urls import path
from .views import create_question, feed_view

urlpatterns=[
    path("creat-ques",create_question,name='create-ques'),
    path("feeds",feed_view,name='feed'),
]