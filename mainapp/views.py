from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from users.models import Follow
from posts.models import Post
from posts.forms import UploadPostForm

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "mainapp/home.html"

    def get(self, request, *args, **kwargs):
        followee_ids = list(Follow.objects.filter(follower=request.user).values_list('followee_id', flat=True))
        followee_ids.append(request.user.id)
        posts = Post.objects.filter(user_id__in=followee_ids).order_by('-created_at').select_related('user', 'user__profile').prefetch_related('tags')
        form = UploadPostForm()
        return self.render_to_response(context={"posts": posts, "form": form})