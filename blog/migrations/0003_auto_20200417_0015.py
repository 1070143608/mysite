# Generated by Django 2.2.7 on 2020-04-16 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_blogtype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_time']},
        ),
    ]
