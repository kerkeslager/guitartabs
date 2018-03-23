from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world")

def detail(request, tab_id):
    return HttpResponse(
        'Tab Id {}'.format(tab_id),
    )
