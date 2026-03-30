from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import *
from .models import *
from questonaries.models import models

# Create your views here.
login_required
def comments(req,id):
    ques = Question.objects.get(id=id)

    if req.method=='POST':
        Comments.objects.create(
            text = req.POST.get('text'),
            q_id = ques,
            user_id = req.user
        )
    return redirect('voting_pole',ques.id)