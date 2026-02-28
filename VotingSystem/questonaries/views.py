from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Category, Question, options
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_question(req):
    if req.method == 'POST':
        ques_text = req.POST.get('ques')
        q_desc = req.POST.get('q_desc')
        ex_date = req.POST.get('ex_date')
        category_id = req.POST.get('cat') 
        user = req.user


        opt_data = req.POST.get('opt_hidden', "")
        opt_dsc_data = req.POST.get('opt_dsc_hidden', "")


        option_list = [item.strip() for item in opt_data.split(",") if item.strip()]
        desc_list = [item.strip() for item in opt_dsc_data.split(",") if item.strip()]

        # Create the Question
        question_obj = Question.objects.create(
            ques=ques_text,
            q_desc=q_desc,
            expiry=ex_date,
            u_id=user
        )

        # Create Options
        for title, dsc in zip(option_list, desc_list):
            options.objects.create(
                option=title,
                o_desc=dsc,
                q_id=question_obj
            )

        messages.success(req, "Poll deployed successfully!")
        return redirect("feed")  

    return render(req, "questionaries/ques_creation.html")

def feed_view(req):
    return render(req,"questionaries/Feed.html")