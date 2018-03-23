from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import deletion

class Tab(models.Model):
    GUITAR = 'guitar'
    BASS = 'bass'
    UKELELE = 'ukelele'
    MIXED = 'mixed'
    OTHER = 'other'

    INSTRUMENT_CHOICES = (
        (GUITAR,    'Guitar'),
        (BASS,      'Bass'),
        (UKELELE,   'Ukelele'),
        (MIXED,     'Mixed'),
        (OTHER,     'Other'),
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=deletion.PROTECT)
    name = models.CharField(max_length=256)
    instrument = models.CharField(
        max_length=16,
        choices=INSTRUMENT_CHOICES,
        default=GUITAR,
    )
    body = models.CharField(max_length=4096)
