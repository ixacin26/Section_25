# profiles/context_processors.py

from followers.models import Follower


def user_counts(request):
    if request.user.is_authenticated:
        user = request.user
        total_followers = Follower.objects.filter(following=user).count()
        total_follows = Follower.objects.filter(followed_by=user).count()
    else:
        total_follows = 0
        total_followers = 0
    return {
        'user_total_follows': total_follows,
        'user_total_followers': total_followers,
    }
