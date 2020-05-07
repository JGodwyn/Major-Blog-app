from django.db import models


class User(models.Model):
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 100)
    description = models.TextField(max_length = 5000)
    categories = models.CharField(max_length = 50)

    def __str__(self):
        return f'{self.username}'


class Posts(models.Model):
    post_link = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'post')
    title = models.CharField(max_length = 200)
    post = models.TextField(max_length = 50000)
    # remember, no_of_posts =  godwin.stuffs.count() ------using godwin as an instance!
    # define that in the views.py file
    date_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.post

    class Meta:
        verbose_name_plural = 'Posts'


class Likes(models.Model):
    likes_link = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name = 'like')
    likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.likes


class Categories(models.Model):
    categories = models.CharField(max_length=100)

    def __str__(self):
        return self.categories





