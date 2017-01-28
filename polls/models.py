from django.db import models


# Create your models here.

class Poll(models.Model):
    name = models.CharField(max_length=45)
    options = models.CharField(max_length=255)


class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    option = models.IntegerField()
    ip = models.CharField(max_length=45)
