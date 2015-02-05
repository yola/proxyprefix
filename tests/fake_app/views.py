from django.core.urlresolvers import reverse
from django.http import HttpResponse


def show_path(request):
    return HttpResponse(reverse('show_path'))
