from django.urls import path
from .views import *


urlpatterns=[
    path('comment/<int:id>/', comments , name='comments'),
    path('comment_reply/<int:id>/',comment_reply,name='comment_reply'),
    path('comment_like/<int:id>/',comments_likes,name='comments_likes'),
    path('post_likes/<int:id>/',post_likes,name='post_likes'),
]