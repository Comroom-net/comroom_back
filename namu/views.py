from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

from .models import Visitor, Room

# Create your views here.


def visitors(request):
    template_name = 'visitors.html'
    context = {}
    context['posts'] = Visitor.objects.order_by('-id')

    return render(request, template_name, context)


def write(request):
    template_name = 'write_post.html'
    context = {}
    if request.method == 'POST':
        room = request.POST.get('room')
        writer = request.POST.get('writer')
        text = request.POST.get('context')
        # image = request.FILES['visitor_image']
        # image resize required
        pw = request.POST.get('pw')
        new_post = Visitor(room=Room.objects.get(room_name=room), writer=writer,
                           visitor_text=text, visitor_pw=pw)
        # if image:
        #     new_post.visitor_image = image
        new_post.save()
        return redirect('/namu/visitors')
    else:
        context['rooms'] = Room.objects.all()

    return render(request, template_name, context)
