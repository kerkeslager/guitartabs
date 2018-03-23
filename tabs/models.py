from django.db import models

class Tab(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    body = models.CharField(max_length=4096)
