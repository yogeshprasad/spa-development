# Generated by Django 2.0.6 on 2018-11-06 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_coachingcontact_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentEnquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=500)),
                ('email', models.EmailField(default='', max_length=70)),
                ('mobile', models.IntegerField(default=0)),
                ('message', models.CharField(default='', max_length=1000)),
                ('subject', models.CharField(default='', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
