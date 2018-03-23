from django import forms
from django.contrib import admin

from . import models

class TabAdminForm(forms.ModelForm):

    class Meta:
        model = models.Tab
        widgets = {
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 50}),
        }

        fields = '__all__'

class TabAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = TabAdminForm

admin.site.register(models.Tab, TabAdmin)
