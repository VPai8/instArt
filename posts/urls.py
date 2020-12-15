from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('', Home.as_view(), name='insta-home'),
    path('create/', CreatePost.as_view(), name='new-post'),
    path('edit/<int:pk>', PostEdit.as_view(), name='edit-post'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete-post'),
    path('people/', People.as_view(), name='people'),
    path('art/<int:pk>', PostDetail.as_view(), name='post'),
    path('follow/<int:id>', follow, name='follow'),
    path('unfollow/<int:id>', unfollow, name='unfollow'),
    path('like/<int:id>', like, name='like'),
    path('unlike/<int:id>', unlike, name='unlike'),
    path('comments/<int:id>', comments, name='comments'),
    path('comment/<int:id>', comment, name='comment'),
    path('userart/', userposts, name='user-posts'),
    path('profile/<int:id>', public_profile, name='public-profile'),
    path('about/', about, name='about'),
]
