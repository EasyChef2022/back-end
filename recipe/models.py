from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    cooking_method = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    cuisine = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    ingredients = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    prep_time = models.IntegerField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    class Meta:
        db_table = 'recipe'
