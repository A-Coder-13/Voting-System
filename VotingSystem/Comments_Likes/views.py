from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import *
from .models import *

# Create your views here.
login_required
def comments(req):
    if req.method=='POST':
        Comments.objects.create(
            text = req.POST.get('text'),
            q_id = req.POST.get('ques'),
            user_id = req.user
        )
    return redirect('voting_pole')