from django.contrib import admin

from . import forms, models

class TabAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = forms.TabAdminForm

admin.site.register(models.Tab, TabAdmin)
