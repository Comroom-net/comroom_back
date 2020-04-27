from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class Nocookie(TemplateView):
    template_name = "youtube_nocookie.html"
