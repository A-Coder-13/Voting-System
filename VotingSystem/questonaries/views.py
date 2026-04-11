from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Category, Question, options,Vote_Click
from Comments_Likes.models import *
from users.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from collections import Counter


def trending_hashtags():
    ques = Question.objects.all()

    tags_list=[]

    for q in ques:
        if q.hashtags:
            tags = q.hashtags.split()
            for tag in tags:
                tags_list.append(tag.strip().lower())
    
    tag_count = Counter(tags_list)

    tag = tag_count.most_common(3)
    
    return tag



# Create your views here.
@login_required
def create_question(req):
    if req.method == 'POST':
        ques_text = req.POST.get('ques')
        q_desc = req.POST.get('q_desc')
        ex_date = req.POST.get('ex_date')
        category_id = req.POST.get('cat') 
        hashtags= req.POST.get('hashtags')
        img = req.FILES.get('img')
        user = req.user

        cat =Category.objects.get(id=category_id)


        # Create the Question
        question_obj = Question.objects.create(
            ques=ques_text,
            q_desc=q_desc,
            hashtags=hashtags,
            expiry=ex_date,
            cat_id=cat,
            img=img,
            u_id=user
        )


        opt_data = req.POST.get('opt_hidden', "")
        opt_dsc_data = req.POST.get('opt_dsc_hidden', "")
        

        option_list=[]
        desc_list=[]
        option = ""
        opt_dsc = ""
        for opt in opt_data:
            if opt != ",":
                option += opt
            else:
                option_list.append(option)
                option=""
        # print(option_list)

        for dsc in opt_dsc_data:
            if dsc != ",":
                opt_dsc += dsc
            else:
                desc_list.append(opt_dsc)
                opt_dsc=""
        # print(desc_list)
        



        # Create Options
        for title, dsc in zip(option_list, desc_list):
            options.objects.create(
                option=title,
                o_desc=dsc,
                q_id=question_obj
            )

        messages.success(req, "Poll deployed successfully!")
        return redirect("feeds")  
    
    cat = Category.objects.all()

    return render(req, "questionaries/ques_creation.html", {'category':cat})




def feed_view(req):
    # print(req.user)
    hashtag = req.GET.get('hashtag')
    feeds = None

    if req.user.is_authenticated:
        feeds = Question.objects.exclude(u_id = req.user,expiry__gt=timezone.now())
    else:
        feeds=Question.objects.all()


    if hashtag:
        feeds =feeds.filter(hashtags__icontains=hashtag)
    
    trend_tags = trending_hashtags()
    print(trend_tags)



    feed_array=[]
    for f in feeds: 
        total = Vote_Click.objects.filter(opt_id__q_id=f).count()
        likes = PostLikes.objects.filter(q_id=f.id).count()
        user_liked = PostLikes.objects.filter(q_id=f.id,user_id=req.user.id).exists()
        feed_array.append({
            'ques_vote_count':total,
            'ques_data':f,
            'likes': likes,
            'user_liked':user_liked
        })

        # print(feed_array)


    context= {
        'feeds':feed_array,
        'trending_tags':trend_tags
        }
    return render(req,"questionaries/Feed.html", context)






@login_required
def voting_pole(req, id):

    user = req.user
    ques = Question.objects.get(id=id)
    opt = options.objects.filter(q_id=ques)

    # check user vote
    user_vote = Vote_Click.objects.filter(
        opt_id__q_id=ques,
        user_id=user
    ).first()

    if req.method == 'POST':

        opt_id = req.POST.get("opt_id")
        selected_opt = options.objects.get(id=opt_id)

        if user_vote:
            messages.warning(req, 'You can vote only once.')
            return redirect('voting_pole', id=id)

        Vote_Click.objects.create(
            opt_id=selected_opt,
            user_id=user
        )

        messages.success(req, 'Vote submitted successfully!')
        return redirect('voting_pole', id=id)

    
    total_vote = Vote_Click.objects.filter(opt_id__q_id=ques).count()

    option = []

    for o in opt:
        vote_count = Vote_Click.objects.filter(
            opt_id=o
        ).count()

        option.append({
            'opt_count': vote_count,
            'opt_data': o
        })
    
    now = timezone.now()
    if ques.expiry > now:
        diff= ques.expiry-now
        # print(diff)
        days = diff.days
        hours = diff.seconds //3600
        minutes = (diff.seconds %3600) //60
        
        remaining_time = f"{days}d {hours}h {minutes}m"
    else:
        remaining_time = "Expired"


    q_comments = Comments.objects.filter(q_id=id)
    comments = []
    for comment in q_comments:
        comments_replies = CommentsReply.objects.filter(comment=comment.id)
        comments_likes = CommentsLikes.objects.filter(c_id=comment.id)
        isUserLikes=CommentsLikes.objects.filter(c_id=comment.id,user_id=req.user.id).exists()
        
        comments.append({
            'comment':comment,
            'replies':comments_replies,
            'likes':comments_likes,
            'isUserLikes':isUserLikes,
        })
    


    context = {
        'ques': ques,
        'opt': option,
        'vote': True if user_vote else False,
        'total': total_vote,
        'user_choice_id': user_vote.opt_id.id if user_vote else None,
        'remaining_time':remaining_time,
        'comments':comments,
    }

    return render(req, "questionaries/voting-pole.html", context)




