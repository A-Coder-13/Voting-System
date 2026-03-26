from django.urls import path
from .views import reg, user_login,user_logout,forget_password,otp,reset_password

urlpatterns=[
    path('regist',reg,name='regis'),
    path('login',user_login,name='login'),
    path('logout',user_logout,name='Logout'),
    path('forget_password',forget_password,name='forget_password'),
    path('otp',otp,name='otp'),
    path('reset_password',reset_password,name='reset_password'),
]
