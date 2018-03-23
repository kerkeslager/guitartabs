from django import forms

from . import models

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
            'body',
        )
        widgets = {
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 50}),
        }
