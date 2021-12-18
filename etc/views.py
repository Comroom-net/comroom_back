import csv
import logging

from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Disabled_ch, Notice_nocookie, RollFile, HTMLpage
from .serializers import NoticeNocookieSerializer, DisabledChannelSerializer
from .GsuiteUsers import GUser, GUser_school


logger = logging.getLogger(__name__)


class NoticeNocookieViewSet(viewsets.ModelViewSet):
    queryset = Notice_nocookie.objects.all()
    serializer_class = NoticeNocookieSerializer


class DisabledChannelViewSet(viewsets.ModelViewSet):
    queryset = Disabled_ch.objects.all()
    serializer_class = DisabledChannelSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Disabled_ch.objects.filter(is_noticed=True)
        return queryset


def nocookie(request):
    template_name = "youtube_nocookie.html"
    context = {}
    chs = Disabled_ch.objects.filter(is_noticed=True)
    context["chs"] = chs
    notice = Notice_nocookie.objects.all()
    if notice:
        context["notice"] = notice[0]

    if request.method == "POST":
        ch_val = request.POST.get("new_ch")
        if Disabled_ch.objects.filter(ch_name=ch_val):
            exist_ch = Disabled_ch.objects.get(ch_name=ch_val)
            exist_ch.is_noticed = True
            exist_ch.save()
        else:
            new_ch = Disabled_ch(ch_name=ch_val)
            new_ch.save()

    return render(request, template_name, context)


@api_view
def GsuiteConvertor(request):
    context = {}

    if request.method == "POST":
        file = request.FILES["roll_file"]
        school = request.POST.get("school")
        result = valid_G(school, file)
        if result.get("valid"):
            s_info = result.get("result")
            grade = request.POST.get("grade")
            classN = request.POST.get("classN")
            file_name = f"{school}{grade}-{classN}_user.csv"
            roll_file = RollFile(title=file_name, roll_file=file)
            roll_file.roll_file.name = file_name
            if request.POST.get("whole_school"):
                guser = GUser_school(file, s_info)
            else:
                guser = GUser(file, s_info, grade, classN)
            roll_file.save()
            context["result"] = guser.file_url
        else:
            context["errors"] = "학교명 혹은 파일이 올바르지 않습니다. 문제가 반복되면 관리자에게 문의해주세요."

    return Response(data=context, status=status.HTTP_200_OK)


def valid_G(school, file):
    s_info = ""
    error_msg = ""
    with open("staticfiles/G-suite/cbe_school_info.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if row[1] == school:
                s_info = [row[0], school, row[2].split("@")[0]]
                break
        error_msg += "학교명({})이 올바르지 않습니다. ".format(school)

    if s_info:
        # Should change .csv to .xlsx when deploy
        if file.size < 100000 and ".xlsx" in file.name:
            return {"valid": True, "result": s_info}
        print(f"{file.name}: {file.size}byte")
        error_msg += "파일 확장자는 .xlsx이고, 용량은 10MB이하여야 합니다. {}".format(file.name)

    return {"valid": False, "error": error_msg}


def load_html(request, **kwargs):
    template_name = "htmlpage.html"
    context = {}
    # context['page'] = HTMLpage.objects.get(title='구구단').page
    context["page"] = HTMLpage.objects.get(id=kwargs["pk"]).page

    return render(request, template_name, context)


def load_last_html(request):
    template_name = "pages.html"
    context = {}

    context["pages"] = HTMLpage.objects.order_by("-id")

    return render(request, template_name, context)


# def load_last_html(request):
#     template_name = "htmlpage.html"
#     context = {}
#     # context['page'] = HTMLpage.objects.get(title='구구단').page
#     context['page'] = HTMLpage.objects.order_by('-id')[0].page

#     return render(request, template_name, context)
