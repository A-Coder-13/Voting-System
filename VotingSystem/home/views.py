from django.shortcuts import render,redirect

# Create your views here.

def home(req):
    user= req.user
    print(user)
    return render(req,'home/home.html',{'user':user})

def explore(req):
    return render(req,'home/explore.html',)