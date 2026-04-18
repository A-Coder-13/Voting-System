from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from questonaries.models import *

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
    return render(req, 'home/Explore.html')