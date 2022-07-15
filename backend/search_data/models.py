from django.db import models
from django.contrib.auth.models import User


class SearchData(models.Model):
    id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=20, null=True, blank=True)
    departureDateTime = models.DateTimeField(null=True, blank=True)
    returnDateTime = models.DateTimeField(null=True, blank=True)
    destination = models.CharField(max_length=20, null=True, blank=True)
    cabin = models.CharField(max_length=20, null=True, blank=True)
    adultNum = models.IntegerField(null=True, blank=True)
    childNum = models.IntegerField(null=True, blank=True)
    infantNum = models.IntegerField(null=True, blank=True)
    returnStatus = models.BooleanField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class BookedTicket(models.Model):
    id = models.AutoField(primary_key=True)
    traveler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ticketData = models.JSONField()

