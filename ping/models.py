from django.db import models
from django.contrib.postgres.fields import ArrayField


# Test model
# Ignore this one, it is only for testing purposes
class GroupMember(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, db_index=True)
    password = models.CharField(max_length=200)
    herbs = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    spices = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    proteins = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
