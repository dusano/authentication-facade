from django.db import models


class Mapping(models.Model):
	plug = models.CharField(max_length = 255, unique = True)
	pattern = models.TextField(blank=True)
	target_url = models.TextField()
	index_page = models.BooleanField(default=False, db_index=True)
	group = models.CharField(max_length = 255, blank=True)
