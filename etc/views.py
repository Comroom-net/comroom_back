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

    if request.method == "POST":
        ch_val = request.POST.get('new_ch')
        if Disabled_ch.objects.filter(ch_name=ch_val):
            exist_ch = Disabled_ch.objects.get(ch_name=ch_val)
            exist_ch.is_noticed = True
            exist_ch.save()
        else:
            new_ch = Disabled_ch(ch_name=ch_val)
            new_ch.save()


    return render(request, template_name, context)
