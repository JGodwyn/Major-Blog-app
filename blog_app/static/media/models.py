from django.db import models


class User(models.Model):
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 100)
    description = models.TextField(max_length = 5000)
    categories = models.CharField(max_length = 50)
    image = models.ImageField( default = r'C:\Users\Godwin\django\Blog\blog_app\static\img\camera-1809-461609.png')

    def __str__(self):
        return f'{self.username}'


class Posts(models.Model):
    post_link = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'post')
    title = models.CharField(max_length = 200)
    post = models.TextField(max_length = 50000)
    likes = models.IntegerField(default = 0)
    # remember, no_of_posts =  godwin.stuffs.count() ------using godwin as an instance!
    # define that in the views.py file
    date_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Posts'


class LikedPost(models.Model):
    liked_post_link = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'liked_list')
    liked_post_id = models.IntegerField(default = None)

    def __str__(self):
        return f'post id: {self.liked_post_id}'


class Comment(models.Model):
    comments_link = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name = 'commented')
    comments = models.TextField(max_length=5000)
    commenter = models.CharField(max_length = 200)

    def __str__(self):
        return f' {self.comments}, {self.commenter} '


class Like(models.Model):
    likes_link = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name = 'like')
    likes = models.IntegerField(default = 0)
    liker = models.CharField(max_length = 200)

    def __str__(self):
        return f'{self.likes}, {self.liker}'
