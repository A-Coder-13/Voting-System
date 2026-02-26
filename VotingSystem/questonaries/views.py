from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Category, Question, options
from django.contrib import messages

# Create your views here.
def create_question(req):
    user = req.user
    
    if user.is_authenticated:
        print(user.username)
    else:
        print("User not logged in")
    return render(req,"questionaries/ques_creation.html")



def feed_view(req):
    return render(req,"questionaries/Feed.html")