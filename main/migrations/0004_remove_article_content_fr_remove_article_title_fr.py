# Generated by Django 5.0.6 on 2024-06-29 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_article_content_fr_article_title_fr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content_fr',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title_fr',
        ),
    ]
