# Generated by Django 3.0.5 on 2020-05-24 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0019_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Features',
        ),
    ]
