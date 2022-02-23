from django.db import models
from django.contrib.postgres.fields import ArrayField


# Test model
# Ignore this one, it is only for testing purposes
class GroupMember(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    class Meta:
        db_table = 'group_member'
