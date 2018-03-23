from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import models

def index(request):
    tabs = models.Tab.objects.order_by('-updated')
    context = { 'tabs': tabs }
    return render(request, 'tabs/index.html', context)

def detail(request, tab_id):
    tab = get_object_or_404(models.Tab, pk=tab_id)
    context = { 'tab': tab }
    return render(request, 'tabs/detail.html', context)

def create(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'tabs/create.html', context)

    if request.method == 'POST':
        tab = models.Tab(
            name=request.POST['name'],
            body=request.POST['body'],
        )
        tab.save()

        return HttpResponseRedirect(reverse('tabs:detail', args=(tab.pk,)))
