# Generated by Django 3.0.5 on 2020-05-24 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0017_delete_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='C:\\Users\\Godwin\\django\\Blog\\blog_app\\static\\media\\favicon.png', upload_to=''),
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
