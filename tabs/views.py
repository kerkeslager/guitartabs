import os.path

from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import forms, models, rendering
from core import util

def index(request):
    instrument_choices = models.Tab.INSTRUMENT_CHOICES
    tabs = models.Tab.objects.order_by('-updated')

    context = {
        'instrument_choices': instrument_choices,
        'page': 'tab_index',
        'tabs': tabs,
    }

    return render(request, 'tabs/index.html', context)

def instrument(request, instrument):
    instrument_choices = models.Tab.INSTRUMENT_CHOICES

    try:
        instrument, human_readable_instrument = next(
            (i, hri) for i, hri in instrument_choices if i == instrument
        )
    except StopIteration:
        raise Http404

    tabs = models.Tab.objects.filter(instrument=instrument).order_by('-updated')

    context = {
        'instrument': instrument,
        'human_readable_instrument': human_readable_instrument,
        'instrument_choices': instrument_choices,
        'tabs': tabs,
    }

    return render(request, 'tabs/index.html', context)

def artist_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('tabs:artist_create'))

    if request.method == 'GET':
        artist_form = forms.ArtistForm()
        context = { 'artist_form': artist_form }
        return render(request, 'tabs/artist_create.html', context)

    if request.method == 'POST':
        artist_form = forms.ArtistForm({
            **util.params_to_dict(request.POST),
            **{ 'user': request.user.pk },
        })

        if artist_form.is_valid():
            artist = artist_form.save()
            return HttpResponseRedirect(reverse('tabs:artist_detail', args=(artist.pk,)))

        context = { 'artist_form': artist_form }
        return render(request, 'tabs/artist_create.html', context)

def artist_detail(request, artist_id):
    artist = get_object_or_404(models.Artist, pk=artist_id)

    context = {
        'artist': artist
    }

    return render(request, 'tabs/artist.html', context)

def artist_index(request):
    artists = models.Artist.objects.all()

    context = {
        'artists': artists,
        'page': 'artist_index',
    }

    return render(request, 'tabs/artist_index.html', context)

def detail(request, tab_id):
    tab = get_object_or_404(models.Tab, pk=tab_id)
    context = {
        'tab': tab
    }
    return render(request, 'tabs/detail.html', context)

def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('tabs:create'))

    if request.method == 'GET':
        tab_form = forms.TabForm()
        context = { 'tab_form': tab_form }
        return render(request, 'tabs/create.html', context)

    if request.method == 'POST':
        tab_form = forms.TabForm({
            **util.params_to_dict(request.POST),
            **{ 'user': request.user.pk },
        })

        if tab_form.is_valid():
            tab = tab_form.save()
            return HttpResponseRedirect(reverse('tabs:detail', args=(tab.pk,)))

        context = { 'tab_form': tab_form }
        return render(request, 'tabs/create.html', context)

def edit(request, tab_id):
    tab = get_object_or_404(models.Tab, pk=tab_id)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('tabs:edit', tab_id=tab.pk))

    if not request.user == tab.user:
        raise PermissionDenied


    if request.method == 'GET':
        tab_form = forms.TabForm(initial=model_to_dict(tab))
        context = { 'tab_form': tab_form }
        return render(request, 'tabs/create.html', context)

    if request.method == 'POST':
        tab_form = forms.TabForm({
            **util.params_to_dict(request.POST),
            **{ 'user': request.user.pk },
        })

        if tab_form.is_valid():
            tab = tab_form.save()
            return HttpResponseRedirect(reverse('tabs:detail', args=(tab.pk,)))

def example(request):
    # TODO Cache this
    with open(os.path.join(os.path.dirname(__file__), 'static/example.txt'), 'r') as f:
        raw = f.read()

    rendered = rendering.render(raw)

    context = {
        'raw': raw,
        'rendered': rendered,
    }
    return render(request, 'tabs/example.html', context)
