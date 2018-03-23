from django import forms

from . import models

class ArtistForm(forms.ModelForm):
    class Meta:
        model = models.Artist
        fields = (
            'name',
            'user',
            'website',
            'wikipedia',
        )
        widgets = {
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 50}),
            'user': forms.HiddenInput(),
        }

class TabAdminForm(forms.ModelForm):
    class Meta:
        model = models.Tab
        fields = '__all__'
        widgets = {
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 50}),
        }

class TabForm(forms.ModelForm):
    class Meta:
        model = models.Tab
        fields = (
            'name',
            'user',
            'instrument',
            'artist',
            'body',
        )
        widgets = {
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 50}),
            'user': forms.HiddenInput(),
        }
