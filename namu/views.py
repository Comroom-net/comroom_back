from io import BytesIO

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

from PIL import Image as pil

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
        try:
            image = request.FILES['visitor_image']
        except:
            image = False
        # image resize required
        image = rescale(image, 700)
        pw = request.POST.get('pw')
        new_post = Visitor(room=Room.objects.get(room_name=room), writer=writer,
                           visitor_text=text, visitor_pw=pw)
        if image:
            new_post.visitor_image = image
        new_post.save()
        return redirect('/namu/visitors')
    else:
        context['rooms'] = Room.objects.order_by('room_name')

    return render(request, template_name, context)


def rescale(image, width):
    # input_file = BytesIO(image.read())
    # img = pil.open(input_file)
    img = pil.open(image)

    src_width, src_height = img.size
    src_ratio = float(src_height) / float(src_width)
    dst_height = round(src_ratio * width)

    img = img.resize((width, dst_height), pil.LANCZOS)
    # image_file = BytesIO()
    img.save(image.name, 'PNG')
    # image.file = image_file
    image.file = img
    # 이게 없으면 에러 난다.
    image.file.name = image.name

    return image
