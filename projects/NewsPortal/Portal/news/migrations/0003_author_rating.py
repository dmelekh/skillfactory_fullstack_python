# Generated by Django 3.2.9 on 2021-11-18 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_rename_category_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
