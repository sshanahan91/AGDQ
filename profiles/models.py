from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Profile(models.Model):
	user_id    = models.CharField(max_length = 15, primary_key=True)
	name       = models.CharField(max_length = 150)
	alias      = models.CharField(max_length = 150)