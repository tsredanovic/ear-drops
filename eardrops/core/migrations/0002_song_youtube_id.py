# Generated by Django 3.2.4 on 2021-06-21 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='youtube_id',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
