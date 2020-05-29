from io import BytesIO

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

from PIL import Image as pil

from .models import Visitor, Room

# Create your views here.
def order(request):
    template_name = 'order_page.html'
    context = {}

    return render(request, template_name, context)

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
            image = rescale(image, 700)  # 이게 없으면 모든 사진이 다 잘됨.

        except:
            image = False
        pw = request.POST.get('pw')
        new_post = Visitor(room=Room.objects.get(room_name=room), writer=writer,
                           visitor_text=text, visitor_pw=pw)
        # image resize required
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

    with pil.open(image) as img:
        # img = image

        src_width, src_height = img.size
        print(f'src_width:{src_width}, src_height:{src_height}')
        src_ratio = float(src_height) / float(src_width)
        dst_height = round(src_ratio * width)

        # img = img.resize((width, dst_height), pil.LANCZOS)
        img = img.resize((width, dst_height))
        print(f'dst_width:{width}, dst_height:{dst_height}')
        # image_file = BytesIO()
        img.save(image.name)  # 여기까지는 다 문제 없음.

        # image.file = image_file
        image.file = img
        # 이게 없으면 에러 난다.
        image.file.name = image.name

    return image
