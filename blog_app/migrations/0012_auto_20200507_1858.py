# Generated by Django 3.0.5 on 2020-05-07 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0011_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='likes_link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='blog_app.Posts'),
        ),
    ]
