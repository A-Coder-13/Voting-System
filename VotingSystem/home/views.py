from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from questonaries.models import *
from Comments_Likes.models import *
from django.utils import timezone
from datetime import timedelta
from collections import Counter

def home(req):
    user = req.user
    now = timezone.now()

    #  Search
    search = req.GET.get('search')

    #  Active questions (not expired)
    questions = Question.objects.filter(expiry__gt=now)

    if search:
        questions = questions.filter(
            Q(ques__icontains=search) |
            Q(hashtags__icontains=search)
        )

    #  Add vote count (assuming related_name='votes')
    questions = questions.annotate(total_votes=Count('options__vote_click')).order_by('-id')[:3]

    #  Trending hashtags logic
    hashtag_dict = {}
    
    for q in Question.objects.all():
        if q.hashtags:
            tags = q.hashtags.split()   # "#django #python"
            for tag in tags:
                tag = tag.strip().lower()
                hashtag_dict[tag] = hashtag_dict.get(tag, 0) + 1

    # Sort hashtags by count
    trending_hashtags = sorted(hashtag_dict.items(), key=lambda x: x[1], reverse=True)[:10]

    context = {
        'user': user,
        'questions': questions,
        'trending_hashtags': trending_hashtags,
        'search': search,
    }

    return render(req, 'home/home.html', context)



def explore(req):
    if req.user.is_authenticated:
        data = Question.objects.exclude(u_id=req.user)
    else:
        data = Question.objects.all()

    
    # Trending question
    today=timezone.now()
    recent_time = today - timedelta(days=-1)
    trending_ques = data.annotate(
        recent_votes = Count(
            'options__vote_click',
            filter=Q(options__vote_click__created_at__gte=recent_time)
        ),
        recent_likes = Count(
            'postlikes',
            filter=Q(postlikes__created_at__gte=recent_time)
        )
    ).order_by('-recent_likes','-recent_votes').first()

    in_debate = Vote_Click.objects.filter(opt_id__q_id=trending_ques.id).count()
    trending_ques={
        'ques':trending_ques,
        'in_debate':in_debate
    }

    # recent ceation
    recent_creation=data.order_by('-created_at').first()

    # Votes_today
    Votes_today = Vote_Click.objects.filter(created_at=today).count()

    # Active Nodes
    active_poles = data.filter(expiry__gte=today).count()
    print(active_poles)

    active_nodes_persentage=(active_poles/data.count())*100
    print(active_nodes_persentage)



    # Category
    cat=Category.objects.filter()
    category=cat.annotate(
        cat=Count('question')
    )
    print(category)


    context={
        'trending_ques': trending_ques,
        'just_created':recent_creation,
        'votes_today':Votes_today,
        'active_poles':active_poles,
        'active_poles_persentage':active_nodes_persentage
    }
    return render(req, 'home/Explore.html',context)