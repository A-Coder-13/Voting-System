from django.urls import path
from .views import *


urlpatterns=[
    path('comment', comments , name='comments')
]