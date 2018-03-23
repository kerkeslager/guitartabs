from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models

def index(request):
    tabs = models.Tab.objects.order_by('-updated')
    context = { 'tabs': tabs }
    return render(request, 'tabs/index.html', context)

def detail(request, tab_id):
    tab = get_object_or_404(models.Tab, pk=tab_id)
    context = { 'tab': tab }
    return render(request, 'tabs/detail.html', context)
