# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Members(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    phone = models.CharField(max_length=255L, blank=True)
    rushset_id = models.IntegerField(null=True, blank=True)
    is_rush_secceed = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    class Meta:
        db_table = 'members'



class Rushset(models.Model):
    id = models.IntegerField(primary_key=True)
    rush_name = models.CharField(max_length=255L, unique=True, blank=True)
    is_finish = models.IntegerField(null=True, blank=True)
    rush_count = models.IntegerField(null=True, blank=True)
    started_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    class Meta:
        db_table = 'rushset'

