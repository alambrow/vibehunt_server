from django.db import models

class Comment(models.Model):
    venueId = models.ForeignKey("Venue", on_delete=models.CASCADE)
    commentId = models.IntegerField()
    timestamp = models.IntegerField()