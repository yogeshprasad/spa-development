from django.db import models

class CoachingProfile(models.Model):
	username = models.CharField(max_length=100, unique=True, blank=False)
	name = models.CharField(max_length=100, default='')
	url = models.CharField(max_length=10, default='')



