# Generated by Django 2.2.5 on 2020-03-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='/static/user.png', upload_to='profile_image'),
        ),
    ]