from django.urls import path
from .views import create_question, feed_view,voting_pole

urlpatterns=[
    path("creat-ques",create_question,name='create-ques'),
    path("feeds",feed_view,name='feeds'),
    path("voting-pole/<int:id>/",voting_pole,name='voting_pole'),
]