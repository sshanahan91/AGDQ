from __future__ import unicode_literals

from django.db import models
from profiles.models import Profile

# Create your models here.

class Tag(models.Model):
	name         = models.CharField(max_length = 150, primary_key=True)

class Run(models.Model):
	run_id       = models.CharField(max_length = 15, primary_key=True)
	event_id     = models.CharField(max_length = 15)
	name         = models.CharField(max_length = 150)
	game         = models.CharField(max_length = 150)
	description  = models.CharField(max_length = 1500)
	started_at   = models.DateTimeField()
	ended_at     = models.DateTimeField()
	youtube_link = models.CharField(max_length = 150)
	tags         = models.ManyToManyField(Tag)
	runners      = models.ManyToManyField(Profile)

# Run_id -> primary key
# Event_id -> foreign key
# Name
# Game - blank
# description
# Started_at
# Ended_at
# ?Bid_war
# Youtube_link
# ??Relation 1:n Tags
# ??Relation - runners m:n
# ??Relation - Bids 1:n
# ??Relation - Prizes m:n
