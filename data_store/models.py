from django.db import models
from authentication.models import User
from datetime import datetime

class Datastore(models.Model):
    search_query = models.CharField(max_length=256, null=True) 
    raw_data = models.JSONField(default=[], null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(default=datetime.now())
    date_updated = models.DateField(default=datetime.now())
    status = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name_plural = "Data Store"

