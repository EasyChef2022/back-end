import json
from json import JSONEncoder

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    cook_time = models.IntegerField(default=0)
    prep_time = models.IntegerField(default=0)
    description = models.CharField(max_length=2000, default="")
    ingredients = ArrayField(models.CharField(max_length=2000), default=list)
    instructions = ArrayField(models.CharField(max_length=2000), default=list)
    photo_url = models.CharField(max_length=400, default="")
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=400, default="")
    recipe_url = models.CharField(max_length=400, default="")

    class Meta:
        db_table = 'recipe'

    class RecipeEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
