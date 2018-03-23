from django.contrib import admin

from . import forms, models

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TabAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = forms.TabAdminForm

admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Tab, TabAdmin)
