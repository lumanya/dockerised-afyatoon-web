# Generated by Django 4.2.7 on 2023-11-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animationepisode',
            name='video',
            field=models.CharField(help_text='Enter video url', max_length=255, null=True),
        ),
    ]
