from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, Http404, get_list_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q


@login_required
def follow(request, id):
    if request.method == 'POST':
        if request.user.id == id:
            raise HttpResponseForbidden()
        else:
            following = get_object_or_404(User, pk=id)
            follower = request.user
            new_follow = Follow(user1=follower, user2=following)
            new_follow.save()
            return JsonResponse({})


@login_required
def unfollow(request, id):
    if request.method == 'POST':
        if request.user.id == id:
            raise HttpResponseForbidden()
        else:
            following = get_object_or_404(User, pk=id)
            follower = request.user
            follow = Follow.objects.filter(user1=follower, user2=following)
            follow.delete()
            return JsonResponse({})


@login_required
def like(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if Like.objects.filter(user=request.user, post=post).exists():
            return JsonResponse({"error": "already liked!"})
        else:
            like = Like(user=request.user, post=post)
            like.save()
            return JsonResponse({'likes': Like.objects.filter(post=post).count()})


@login_required
def unlike(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if Like.objects.filter(user=request.user, post=post).exists():
            like = Like.objects.filter(user=request.user, post=post)
            like.delete()
            return JsonResponse({'likes': Like.objects.filter(post=post).count()})
        else:
            return JsonResponse({"error": "like to unlike!"})


@login_required
def comments(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post=post).order_by('-last_edit')
        comments_json = [{'comment': comment.comment,
                          'username': comment.user.username,
                          'userimg': comment.user.profile.image.url}

                         for comment in comments]
        return JsonResponse(comments_json, safe=False)


@login_required
def userposts(request):
    if request.method == 'GET':
        posts = request.user.post_set.all().order_by("-last_edit")
        liked_posts = [like.post for like in request.user.like_set.all()]
        context = {}
        context['arts'] = [{'post': post,
                            'liked': post in liked_posts,
                            'likes': Like.objects.filter(post=post).count(),
                            'commentc': post.comment_set.all().count()}
                           for post in posts]
        return render(request, 'posts/userposts.html', context=context)


@login_required
def public_profile(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        posts = user.post_set.all()
        liked_posts = [like.post for like in request.user.like_set.all()]
        context = {}
        context['arts'] = [{'post': post,
                            'liked': post in liked_posts,
                            'likes': Like.objects.filter(post=post).count(),
                            'commentc': post.comment_set.all().count(),
                            }
                           for post in posts]
        context['user'] = user
        context['followers'] = Follow.objects.filter(user2=user).count()
        context['following'] = Follow.objects.filter(user1=user).count()
        return render(request, 'posts/public_profile.html', context=context)


@login_required
def comment(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        comment = Comment.objects.create(
            user=request.user, post=post, comment=request.POST['comment'])
        return JsonResponse({"comment": comment.comment,
                             'username': comment.user.username,
                             'userimg': comment.user.profile.image.url,
                             'commentc': post.comment_set.all().count()})


@login_required
def about(request):
    return render(request, 'posts/about.html')


class Home(LoginRequiredMixin, ListView):
    template_name = 'posts/home.html'
    paginate_by = 3

    def get_queryset(self):
        squery = self.request.GET.get('search')
        following = self.request.user.follower.all()
        users = [follow.user2 for follow in following]
        users.append(self.request.user)
        self.queryset = Post.objects.filter(
            user__in=users).order_by('-last_edit')
        if squery != None and squery != "":
            filters = Q(title__icontains=squery) | Q(
                desc__icontains=squery) | Q(user__username__icontains=squery)
            self.queryset = self.queryset.filter(
                filters).order_by('-last_edit')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes = self.request.user.like_set.all()
        liked_posts = [like.post for like in likes]
        list_arts = [{'post': post,
                      'liked': post in liked_posts,
                      'likes': Like.objects.filter(post=post).count(),
                      'commentc': post.comment_set.all().count()}
                     for post in self.queryset]

        paginator = Paginator(list_arts, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            arts = paginator.page(page)
        except PageNotAnInteger:
            arts = paginator.page(1)
        except EmptyPage:
            arts = paginator.page(paginator.num_pages)
        context['arts'] = arts
        return context


class CreatePost(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    template_name = 'posts/newpost.html'
    fields = ['image', 'title', 'desc']
    success_url = reverse_lazy('insta-home')
    success_message = 'Post created!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        liked_users = [like.user for like in post.like_set.all()]
        context['art'] = {'post': post,
                          'liked': self.request.user in liked_users,
                          'likes': Like.objects.filter(post=post).count(),
                          'commentc': post.comment_set.all().count()}
        return context


class PostEdit(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/post_edit.html'
    fields = ['title', 'desc']
    success_message = 'Post updated!'

    def get_success_url(self):
        return self.request.path

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostDelete(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('user-posts')
    success_message = 'Post deleted!'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        data_to_return = super(PostDelete, self).delete(
            request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return data_to_return


class People(LoginRequiredMixin, ListView):
    model = User
    template_name = 'posts/people.html'

    def get_queryset(self):
        squery = self.request.GET.get('search')
        self.queryset = User.objects.filter(
            is_staff=False, is_superuser=False).exclude(username=self.request.user.username)
        if squery != None and squery != "":
            self.queryset = self.queryset.filter(username__icontains=squery)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        people = self.queryset
        cur_user = User.objects.get(username=self.request.user.username)
        following = cur_user.follower.all()
        following = {follow.user2.username for follow in following}
        is_following = [
            True if person.username in following else False for person in people]
        people_with_follow = [
            {'user': people[i], 'is_following':is_following[i]} for i in range(len(people))]
        people_with_follow = sorted(
            people_with_follow, key=lambda i: i['is_following'])

        context['people1'] = [people_with_follow[i]
                              for i in range(len(people)) if i % 3 == 0]
        context['people2'] = [people_with_follow[i]
                              for i in range(len(people)) if i % 3 == 1]
        context['people3'] = [people_with_follow[i]
                              for i in range(len(people)) if i % 3 == 2]
        return context
