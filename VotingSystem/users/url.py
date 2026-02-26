from django.urls import path
from .views import reg, user_login,user_logout

urlpatterns=[
    path('regist',reg,name='regis'),
    path('login',user_login,name='login'),
    path('logout',user_logout,name='logout'),
]