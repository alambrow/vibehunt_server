from django.db import models

class Venue(models.Model):
    venId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()