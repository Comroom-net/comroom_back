from django.shortcuts import render

# Create your views here.
def apply_page(request):
    template_page = "apply_lecture.html"

    return render(request, template_page)