from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Disabled_ch

# Create your views here.


class Nocookie(TemplateView):
    template_name = "youtube_nocookie.html"

def nocookie(request):
    template_name = "youtube_nocookie.html"
    context = {}
    chs = Disabled_ch.objects.filter(is_noticed=True)
    context['chs'] = chs

    return render(request, template_name, context)
