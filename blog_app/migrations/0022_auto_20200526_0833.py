# Generated by Django 3.0.5 on 2020-05-26 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0021_likedpost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likedpost',
            old_name='liked_post',
            new_name='liked_post_id',
        ),
    ]
