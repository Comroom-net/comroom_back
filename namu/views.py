import os
import json
from io import BytesIO

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from PIL import Image as pil
import telegram

from .models import Visitor, Room

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secret File Control
telegram_file = os.path.join(BASE_DIR, 'bot_info.json')

with open(telegram_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        erro_msg = f"Set the {setting} environment variable"
        raise ImproperlyConfigured(erro_msg)

# Create your views here.


def order(request):
    if request.session['room'] == '':
        return render(request, "order_fail.html", {})
    template_name = 'order_page.html'
    context = {}

    return render(request, template_name, context)


class order_success(TemplateView):
    template_name = 'order_success.html'


class Namu_intro(TemplateView):
    template_name = 'namu_intro.html'


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


def msg_test(request, *args, **kwargs):
    test_token = get_secret("demo_token")
    test_bot = telegram.Bot(token=test_token)
    test_room = get_secret("demo_id")
    msg = 'test'
    if request.method == "POST":
        msg = request.POST.get('order_list')
        test_bot.sendMessage(chat_id=test_room, text=msg)
    else:
        test_bot.sendMessage(chat_id=test_room, text=msg)

    return redirect('/namu/order')


def order_msg(request, *args, **kwargs):
    test_token = get_secret("namu_token")
    # test_token = get_secret("demo_token")
    test_bot = telegram.Bot(token=test_token)
    test_room = get_secret("namu_id")
    # test_room = get_secret("demo_id")
    msg = 'test'
    if request.method == "POST":
        msg = request.POST.get('order_list')
        room = request.session['room']
        if room != '':
            room = f"{room}) \n"
        else:
            # order fail page here
            return render(request, "order_fail.html", {})
        msg = room + msg
        test_bot.sendMessage(chat_id=test_room, text=msg)
    else:
        # order fail page here
        return render(request, "order_fail.html", {})
    request.session['room'] = ''

    return redirect('/namu/order_success')


def room_auth(request, *args, **kwargs):
    request.session['room'] = kwargs['room']

    return redirect('/namu/order')
