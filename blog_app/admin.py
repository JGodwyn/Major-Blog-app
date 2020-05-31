from django.contrib import admin
from .models import User, Posts, LikedPost, Comment, Like


class User_display(admin.ModelAdmin):
    list_display = ('username', 'description', 'categories')


class Posts_display(admin.ModelAdmin):
    list_display = ('post_link', 'title', 'post','likes',  'date_created')


class Likes_display(admin.ModelAdmin):
    list_display = ('liked_post_link', 'liked_post_id')


class Comment_display(admin.ModelAdmin):
    list_display = ('comments_link', 'comments', 'commenter')


class Like_display(admin.ModelAdmin):
    list_display = ('likes', 'liker')


admin.site.register(User, User_display)
admin.site.register(Posts, Posts_display)
admin.site.register(LikedPost, Likes_display)
admin.site.register(Comment, Comment_display)
admin.site.register(Like, Like_display)
