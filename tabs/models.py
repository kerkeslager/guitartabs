from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import deletion

class Tab(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=deletion.PROTECT)
    name = models.CharField(max_length=256)
    body = models.CharField(max_length=4096)
