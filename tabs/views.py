from django.http import HttpResponse
from django.shortcuts import render

from . import models

def index(request):
    tabs = models.Tab.objects.order_by('-updated')
    context = { 'tabs': tabs }
    return render(request, 'tabs/index.html', context)

def detail(request, tab_id):
    tab = models.Tab.objects.get(pk=tab_id)
    context = { 'tab': tab }
    return render(request, 'tabs/detail.html', context)
