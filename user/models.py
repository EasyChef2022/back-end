from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True, db_index=True, null=False, blank=False)
    password = models.CharField(max_length=200)
    herbs = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    spices = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)
    proteins = ArrayField(ArrayField(models.CharField(max_length=200), default=list, size=3), default=list, null=True)

    class Meta:
        db_table = 'user'
