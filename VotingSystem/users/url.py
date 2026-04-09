from django.urls import path
from .views import *

urlpatterns=[
    path('regist',reg,name='regis'),
    path('login',user_login,name='login'),
    path('logout',user_logout,name='Logout'),
    path('forget_password',forget_password,name='forget_password'),
    path('otp',otp,name='otp'),
    path('reset_password',reset_password,name='reset_password'),
    path('edit_profile',edit_profile,name='edit_profile'),
    path('profile',profile_view,name='profile'),
    path('user_profile/<int:id>',other_profile_view,name='user_profile'),
]
