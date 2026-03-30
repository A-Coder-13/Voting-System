from django.urls import path
from .views import *


urlpatterns=[
    path('comment/<int:id>/', comments , name='comments')
]