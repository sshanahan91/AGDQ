from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Event(models.Model):
	event_id   = models.CharField(max_length = 15)
	name       = models.CharField(max_length = 150)
	started_at = models.DateTimeField()
	ended_at   = models.DateTimeField()