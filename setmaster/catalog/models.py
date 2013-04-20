from django.db import models
from django.contrib.auth import get_user_model


class Item(models.Model):
    identifier = models.IntegerField()  # this can be a multiverse_id
    quantity = models.IntegerField()
    name = models.CharField(max_length=255)


class Catalog(models.Model):
    name = models.CharField(max_length=255, default="New Catalog")
    user = models.ForeignKey(get_user_model())
    items = models.ManyToManyField(Item)
