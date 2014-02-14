from django.db import models


class Mapping(models.Model):
	plug = models.CharField(max_length = 255, unique = True)
	target_url = models.CharField(max_length = 765, db_index = True)
