from django.db import models


class Mapping(models.Model):
	plug = models.CharField(max_length = 255, unique = True)
	target_url = models.CharField(max_length = 700, db_index = True)
	index_page = models.BooleanField(default=False, db_index=True)
	group = models.CharField(max_length = 255, blank=True)
