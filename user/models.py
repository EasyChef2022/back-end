import json
from json import JSONEncoder

from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True, db_index=True, null=False, blank=False)
    password = models.CharField(max_length=200)
    herbs = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    spices = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    vegetables = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    proteins = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    favorite = ArrayField(models.CharField(max_length=200), default=list, null=True)
    ban = ArrayField(models.IntegerField(), default=list, null=True)

    class UserEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    class Meta:
        db_table = 'user'


