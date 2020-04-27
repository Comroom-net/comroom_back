from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def nocookie_link(request):

    pass

class Nocookie(TemplateView):
    template_name = "youtube_nocookie.html"