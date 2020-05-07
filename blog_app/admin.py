from django.contrib import admin
from .models import User, Posts, Likes


class User_display(admin.ModelAdmin):
    list_display = ('username', 'description', 'categories')


class Posts_display(admin.ModelAdmin):
    list_display = ('post_link', 'title', 'post', 'date_created')


class Likes_display(admin.ModelAdmin):
    list_display = ('likes_link', 'likes')


admin.site.register(User, User_display)
admin.site.register(Posts, Posts_display)
admin.site.register(Likes, Likes_display)
