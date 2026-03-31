from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import *
from .models import *
from questonaries.models import models

# Create your views here.
def comments(req,id):
    ques = Question.objects.get(id=id)

    if req.method=='POST':
        Comments.objects.create(
            text = req.POST.get('text'),
            q_id = ques,
            user_id = req.user
        )
    return redirect('voting_pole',ques.id)



def comment_reply(req,id):
    comment = Comments.objects.get(id=id)

    CommentsReply.objects.create(
        text = req.POST.get("text"),
        user_id = req.user,
        comment=comment,
    )

    return redirect('voting_pole', comment.q_id.id)