from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class QueueItem(models.Model):
	item_name = models.CharField(max_length=200)
	item_type = models.CharField(max_length=200)
	item_id = models.CharField(max_length=200)
	queued_time = models.DateTimeField('time queued')
	place_in_line = models.IntegerField(blank=True)
	queued_by = models.IntegerField(default=None)
	def __str__(self):
		return self.item_name

