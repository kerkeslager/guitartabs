from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import deletion

class Artist(models.Model):
    name = models.CharField(max_length=256, unique=True, null=False, blank=False)

    @property
    def tabs(self):
        return Tab.objects.filter(artist=self).order_by('-created')

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
    artist = models.ForeignKey(Artist, on_delete=deletion.PROTECT, null=True)
    name = models.CharField(max_length=256)
    instrument = models.CharField(
        max_length=16,
        choices=INSTRUMENT_CHOICES,
        default=GUITAR,
    )
    body = models.CharField(max_length=4096)
