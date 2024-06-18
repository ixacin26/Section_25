from django.contrib.auth.models import User
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required
from .forms import UpdateUserForm, UpdateProfileForm

from feed.models import Post
from followers.models import Follower

# Create your views here.

class ProfileDetailView(DetailView):
  http_method_names = ["get"]
  template_name = "profiles/detail.html"
  model = User
  context_object_name = "user"
  slug_field = "username"
  slug_url_kwarg = "username"

  def dispatch(self, request, *args, **kwargs):
    self.request = request
    return super().dispatch(request, *args, **kwargs)


  def get_context_data(self, **kwargs):
    profile_user=self.get_object()
    context = super().get_context_data(**kwargs)
    context["total_posts"] = Post.objects.filter(author=profile_user).count()
    # TODO final project with help from chatgpt
    context["total_followers"] = Follower.objects.filter(following=profile_user).count()
    context["total_follows"] = Follower.objects.filter(followed_by=profile_user).count()
    if self.request.user.is_authenticated:
      context["you_follow"] = Follower.objects.filter(following=profile_user, followed_by=self.request.user).exists()
    return context
  
  
  
class FollowView(LoginRequiredMixin, View):
  http_method_names=["post"]

  def post(self, request, *args, **kwargs):
    data = request.POST.dict()

    if "action" not in data or "username" not in data:
      return HttpResponseBadRequest("Missing data")
    
    try:
      other_user = User.objects.get(username = data["username"])
    except User.DoesNotExist:
      return HttpResponseBadRequest("Missing User")
  
    if data["action"] == "follow":
      # follow
      follower, created = Follower.objects.get_or_create(
        followed_by=request.user,
        following=other_user
      )
    else:
      # unfollow
      try:
        follower = Follower.objects.get(
        followed_by=request.user,
        following=other_user,
        )
      except Follower.DoesNotExist:
        follower=None

      if follower:
        follower.delete()

    return JsonResponse({
      'done': True,
      "wording": "Unfollow" if data["action"] == "follow" else "Follow",
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profiles:detail', username=request.user.username)  # Redirect to the user's profile page

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profiles/update_profile.html', context)