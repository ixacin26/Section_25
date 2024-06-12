# til/context_processors.py
from django.contrib.auth.models import User
from followers.models import Follower


def follower_counts(request):
    if request.user.is_authenticated:
        total_follows = Follower.objects.filter(followed_by=request.user).count()
        total_followers = Follower.objects.filter(following=request.user).count()
    else:
        total_follows = 0
        total_followers = 0
    return {
        'total_follows': total_follows,
        'total_followers': total_followers,
    }
