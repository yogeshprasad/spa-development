# Generated by Django 2.0.6 on 2018-11-08 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20181108_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachingaboutus',
            name='aboutteam',
            field=models.CharField(default='', max_length=5000),
        ),
    ]