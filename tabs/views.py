from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import forms, models

def index(request):
    tabs = models.Tab.objects.order_by('-updated')
    context = { 'tabs': tabs }
    return render(request, 'tabs/index.html', context)

def detail(request, tab_id):
    tab = get_object_or_404(models.Tab, pk=tab_id)
    context = { 'tab': tab }
    return render(request, 'tabs/detail.html', context)

def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login') + '?next=' + reverse('tabs:create'))

    if request.method == 'GET':
        tab_form = forms.TabForm()
        context = { 'tab_form': tab_form }
        return render(request, 'tabs/create.html', context)

    if request.method == 'POST':
        tab = models.Tab(
            user=request.user,
            name=request.POST['name'],
            body=request.POST['body'],
        )
        tab.save()

        return HttpResponseRedirect(reverse('tabs:detail', args=(tab.pk,)))

def edit(request, tab_id):
    tab = get_object_or_404(models.Tab, pk=tab_id)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login') + '?next=' + reverse('tabs:edit', tab_id=tab.pk))

    if not request.user == tab.user:
        raise PermissionDenied


    if request.method == 'GET':
        tab_form = forms.TabForm(initial=model_to_dict(tab))
        context = { 'tab_form': tab_form }
        return render(request, 'tabs/create.html', context)

    if request.method == 'POST':
        tab = models.Tab(
            user=request.user,
            name=request.POST['name'],
            body=request.POST['body'],
        )
        tab.save()

        return HttpResponseRedirect(reverse('tabs:detail', args=(tab.pk,)))
