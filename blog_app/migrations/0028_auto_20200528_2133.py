# Generated by Django 3.0.5 on 2020-05-28 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0027_comment_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('liker', models.CharField(max_length=200)),
                ('likes_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='blog_app.Posts')),
            ],
        ),
    ]
