import datetime
import random
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from django_filters import rest_framework as filters
from google.oauth2 import id_token
from google.auth.transport import requests

from .forms import (
    RegisterForm,
    LoginForm,
    ComroomAdminForm,
    PasswordResetForm,
    GetAdminForm,
    LoginForm_multi,
)
from .models import School, AdminUser, Notice, Comroom, IPs
from .serializers import (
    SchoolSerializer,
    ComroomSerializer,
    AdminUserSerializer,
    NoticeSerializer,
)

from .multiforms import MultiFormsView


logger = logging.getLogger(__name__)

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class ComroomViewSet(viewsets.ModelViewSet):
    queryset = Comroom.objects.all()
    serializer_class = ComroomSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.filter(isshow=True)
    serializer_class = NoticeSerializer


class SchoolView(APIView):
    def post(self, request):
        with transaction.atomic():

            school = School(
                province=request.data.get("province"),
                name=request.data.get("schoolName") + "초등학교",
                ea=request.data.get("ea"),
                s_code=random.randint(1000, 9999),
            )
            school.save()
            adminUser = AdminUser(
                school=school,
                user=request.data.get("user"),
                password=make_password(request.data.get("password")),
                realname=request.data.get("realname"),
                email=request.data.get("email"),
                auth_key=randstr(50),
                is_active=False,
            )
            # TODO: handle follow 2 lines
            self.request.session["username"] = adminUser.realname
            self.request.session["user_id"] = adminUser.user

            adminUser.save()
            for i in range(int(request.data.get("ea"))):
                comroom = Comroom(
                    school=school,
                    roomNo=i + 1,
                    name=f"컴{i+1}실",
                    caption="위치, 교실 이용방법, 이용시 주의사항 등",
                )
                comroom.save()
            mail_title = "컴룸닷컴 가입 인증메일"
            mail_args = {
                "name": adminUser.realname,
                "mail_link": adminUser.auth_key,
                "web_url": settings.WEB_URL,
            }
            mail_context = "컴룸닷컴 가입 인증메일"
            mail_html = render_to_string("mail_template.html", mail_args)
            send_mail(
                mail_title,
                mail_context,
                "ssamko@kakao.com",
                [adminUser.email],
                html_message=mail_html,
            )
            message = f"{adminUser.realname} 선생님께서 입력하신 메일({adminUser.email})로 인증 링크를 발송했습니다. \
                <a href='/FAQ/' role='button' class='btn btn-info'>이메일 인증을 하는 이유</a>"

        return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
def login_api(request):
    user = request.data.get("user")
    if not user:
        return Response("no id input", status=status.HTTP_404_NOT_FOUND)

    password = request.data.get("password")
    if not password:
        return Response("no password input", status=status.HTTP_404_NOT_FOUND)

    try:
        # username 으로 indexing
        admin_user = AdminUser.objects.get(user=user)
    except AdminUser.DoesNotExist:
        return Response("incorrect id", status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, admin_user.password):
        return Response("wrong password", status=status.HTTP_404_NOT_FOUND)

    user_data = {
            "username": admin_user.realname,
            "user_id": admin_user.user,
            "school": admin_user.school.name,
            "s_code": admin_user.school.s_code,
            "is_active": admin_user.is_active,
        }

    return Response(data=user_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def ex_login_api(request):
    user = AdminUser.objects.get(user="icic")
    data = {
        "username": "박새로이",
        "user_id": "icic",
        "school": user.school.name,
        "s_code": user.school.s_code,
        "is_active": user.is_active,
    }

    return JsonResponse(data=data)


@api_view(["GET"])
def user_active_api(request, token):
    # adminUser = get_object_or_404(AdminUser, auth_key=token)
    try:
        adminUser = AdminUser.objects.get(auth_key=token)
    except ObjectDoesNotExist:
        return JsonResponse(
            data={"message": "wrong access"}, status=status.HTTP_400_BAD_REQUEST
        )
    if adminUser.reg_date < datetime.datetime.now() - datetime.timedelta(hours=3):
        deleted_school = adminUser.school.delete()
        logger.debug(f"[deleted school]{deleted_school}")
        message = "만료된 링크입니다. 다시 가입을 신청하세요"
        return JsonResponse(
            data={"message": message}, status=status.HTTP_501_NOT_IMPLEMENTED
        )
    else:
        adminUser.is_active = True
        adminUser.auth_key = ""
        adminUser.save()
        user_data = {
            "username": adminUser.realname,
            "user_id": adminUser.user,
            "school": adminUser.school.name,
            "s_code": adminUser.school.s_code,
            "is_active": adminUser.is_active,
        }
    return JsonResponse(data=user_data, status=status.HTTP_200_OK)


# TODO: remove csrf_exempt
@csrf_exempt
def token_signin(request):
    if request.method == "POST":
        token = request.POST.get("idtoken")
        CLIENT_ID = (
            "480648197974-nbh21s3q24p0hkef3glj7cf2ipvkbl5d.apps.googleusercontent.com"
        )
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo["sub"]
            logger.debug(userid)
            logger.debug(idinfo)
            user = User.objects.get_by_natural_key("ssamko")
            refresh = RefreshToken.for_user(user)
            logger.debug(f"refresh: {str(refresh)}")
            logger.debug(f"access: {str(refresh.access_token)}")
            return JsonResponse(status=status.HTTP_200_OK, data={"good": "success"})
        except ValueError:
            # Invalid token
            logger.debug("invalid token")
            pass
    else:
        return JsonResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def privacy_agree(request):
    template_name = "privacy.html"

    file_path = finders.find("com_privacy.txt")
    searched_location = finders.searched_locations
    f = open(file_path, "r")
    data = f.read()
    f.close()

    return render(request, template_name, {"privacy": data})


def agree_pirv(request):
    request.session["privacy"] = True
    return redirect("/school/register")


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/"

    def get(self, request, *args, **kwargs):
        # 정상적인 방법(개인정보동의)으로 접근했는지 판단
        try:
            privacy = request.session["privacy"]
        except:
            logger.debug("No privacy session")
            return redirect("/")
        else:
            if not privacy:
                return redirect("/")
        return super().get(self, request, args, kwargs)

    def form_valid(self, form):
        with transaction.atomic():

            school = School(
                province=form.cleaned_data.get("province"),
                name=form.cleaned_data.get("name") + "초등학교",
                ea=form.cleaned_data.get("ea"),
                s_code=random.randint(1000, 9999),
            )
            school.save()
            adminUser = AdminUser(
                school=school,
                user=form.cleaned_data.get("user"),
                password=make_password(form.cleaned_data.get("password")),
                realname=form.cleaned_data.get("realname"),
                email=form.cleaned_data.get("email"),
                auth_key=randstr(50),
                is_active=False,
            )
            self.request.session["username"] = adminUser.realname
            self.request.session["user_id"] = adminUser.user
            adminUser.save()
            for i in range(int(form.cleaned_data.get("ea"))):
                comroom = Comroom(
                    school=school,
                    roomNo=i + 1,
                    name=f"컴{i+1}실",
                    caption="위치, 교실 이용방법, 이용시 주의사항 등",
                )
                comroom.save()
            mail_title = "컴룸닷컴 가입 인증메일"
            mail_args = {"name": adminUser.realname, "mail_link": adminUser.auth_key}
            mail_context = "컴룸닷컴 가입 인증메일"
            mail_html = render_to_string("mail_template.html", mail_args)
            send_mail(
                mail_title,
                mail_context,
                "ssamko@kakao.com",
                [adminUser.email],
                html_message=mail_html,
            )
            message = f"{adminUser.realname} 선생님께서 입력하신 메일({adminUser.email})로 인증 링크를 발송했습니다. \
                <a href='/FAQ/' role='button' class='btn btn-info'>이메일 인증을 하는 이유</a>"

        # privacy 세션 초기화
        self.request.session["privacy"] = False
        return render(self.request, "notice.html", {"message": message})
        # return super().form_valid(form)



# TODO: csrf token handling API
@csrf_exempt
@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")
    if not email:
        logger.debug("no email input")
        return Response("no email input", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    teacher_name = request.data.get("teacher_name")
    if not teacher_name:
        return Response("no name input", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    try:
        # indexing by email and realname
        admin_user = AdminUser.objects.get(email=email, realname=teacher_name)
    except AdminUser.DoesNotExist:
        return Response("wrong input info", status=status.HTTP_400_BAD_REQUEST)

    request.session["adminUser_pk"] = admin_user.pk

    logger.debug("forgot password good")
    # send_password_mail(request)

    return Response("good", status=status.HTTP_200_OK)


class MultipleFormsLoginView(MultiFormsView):
    template_name = "login.html"
    form_classes = {
        "login": LoginForm_multi,
        "get_admin": GetAdminForm,
    }

    success_urls = {
        "login": reverse_lazy("index"),
        "get_admin": reverse_lazy("send_password_mail"),
    }

    # actual login
    def login_form_valid(self, form):
        user = form.cleaned_data.get("user")
        password = form.cleaned_data.get("password")
        form_name = form.cleaned_data.get("action")
        logger.debug(user)
        user = AdminUser.objects.get(user=user)
        # set session value
        self.request.session["username"] = user.realname
        self.request.session["user_id"] = user.user
        self.request.session["school"] = user.school.id
        return HttpResponseRedirect(self.get_success_url(form_name))

    # reset password
    def get_admin_form_valid(self, form):
        logger.debug("form valid")
        email = form.cleaned_data.get("email")
        teacher_name = form.cleaned_data.get("teacher_name")
        adminUser = AdminUser.objects.get(email=email, realname=teacher_name)
        form_name = form.cleaned_data.get("action")
        self.request.session["adminUser_pk"] = adminUser.pk
        logger.debug(adminUser)

        return HttpResponseRedirect(self.get_success_url(form_name))


def ex_login(request):
    request.session["username"] = "박새로이"
    request.session["user_id"] = "icic"
    request.session["school"] = AdminUser.objects.get(user="icic").school.id
    return redirect("/")


def logout(request):
    if "username" in request.session:
        del request.session["username"]
        del request.session["user_id"]

    return redirect("/")


def ip_getter(request):
    try:
        ip_addr = request.META["REMOTE_ADDR"]
    except:
        logger.debug("localhost")
    else:

        try:
            this_ip = IPs.objects.get(ip=ip_addr)
        except:
            new_ip = IPs(
                ip=ip_addr,
            )
            if request.session["school"]:
                new_ip.school = School.objects.get(id=request.session["school"])
            new_ip.save()
        else:

            this_ip.ip_count += 1
            this_ip.save()


def index(request):
    # ip_getter(request)
    context = {}

    username = request.session.get("username")
    user_id = request.session.get("user_id")

    # get notice objects
    notices = Notice.objects.filter(isshow=True)
    context["notices"] = notices

    if username:
        try:
            adminUser = AdminUser.objects.get(realname=username, user=user_id)
            school = adminUser.school
            context["username"] = username
            context["school"] = school.name
            context["s_code"] = school.s_code
            context["is_active"] = adminUser.is_active
            request.session["school_info"] = school.id
        except:
            redirect("/")

    elif "s_code" in request.session:
        context["s_code"] = request.session["s_code"]

    return render(request, "index.html", context)


class AboutView(TemplateView):
    template_name = "about.html"


class ComroomAdminView(View):
    template_name = "comroom_admin.html"
    success_url = "/"
    context = {}

    def get(self, request, *args, **kwargs):
        context = self.context
        forms = []
        try:
            school = School.objects.get(id=request.session["school_info"])
        except:
            redirect("/")

        for i in range(school.comroom_set.count()):
            room = school.comroom_set.get(roomNo=i + 1)
            # initial form by getting data from DB
            comform = ComroomAdminForm(
                initial={
                    "room_name": room.name,
                    "room_caption": room.caption,
                }
            )
            # form_name = 'form'+str(i+1)

            forms.append(comform)

        context["forms"] = forms

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.context
        forms = []

        school = School.objects.get(id=request.session["school_info"])

        for i in range(school.comroom_set.count()):

            # bind form with instance
            form = school.comroom_set.get(roomNo=i + 1)
            logger.debug(form)
            logger.debug(request.POST)
            form.name = request.POST["room_name" + str(i + 1)]
            form.caption = request.POST["room_caption" + str(i + 1)]
            form.save()

        return redirect("/")

    def form_valid(self, form):
        return super().form_valid(form)


# 새로 생긴 컴퓨터룸 table에 학교별 데이터 생성하기 위한 함수


def make_room(request):
    schools = School.objects.all()
    for school in schools:
        for room in range(school.ea):

            a = Comroom(
                school=school, name=f"컴{room+1}실", caption="위치, 이용안내 등", roomNo=room + 1
            )
            # 이미 존재하는지 검사
            if not Comroom.objects.filter(school=school, roomNo=room + 1).exists():
                a.save()

    return redirect("/")


def time_admin(request):
    template_name = "time_admin.html"
    context = {}
    times = []

    school = School.objects.get(id=request.session["school_info"])
    timetables = school.timetable_set.all().order_by("-date")

    for i in range(timetables.count()):
        times.append(timetables[i])

    context["times"] = times

    return render(request, template_name, context)
    # return redirect('/')


def del_time(request, **kwargs):

    school = School.objects.get(id=request.session["school_info"])
    timetables = school.timetable_set.all().order_by("-date")
    timetables[kwargs["i"]].delete()

    return redirect("/time_admin/")


# token init. method


def randstr(length):
    rstr = "0123456789abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ"
    rstr_len = len(rstr) - 1
    result = ""
    for i in range(length):
        result += rstr[random.randint(0, rstr_len)]
    return result


def user_active(request, token):
    adminUser = get_object_or_404(AdminUser, auth_key=token)
    if adminUser.reg_date < datetime.datetime.now() - datetime.timedelta(hours=3):
        adminUser.school.delete()
        message = "만료된 링크입니다. 다시 가입을 신청하세요"
    else:
        adminUser.is_active = True
        adminUser.auth_key = ""
        adminUser.save()
        message = "인증되었습니다. 불편한 사항은 언제든 말씀해주세요 ^^"
    return render(request, "notice.html", {"message": message})


def reset_password(request, token):
    adminUser = get_object_or_404(AdminUser, auth_key=token)

    if request.method == "GET":
        reset_form = PasswordResetForm()
        return render(
            request,
            "reset_password.html",
            {"teacher_name": adminUser.realname, "form": reset_form},
        )
    else:
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            adminUser.password = make_password(reset_form.cleaned_data.get("password"))
            adminUser.auth_key = ""
            adminUser.save()
            request.session["user_id"] = adminUser.user
            request.session["username"] = adminUser.realname
            request.session["school"] = adminUser.school.id
            return redirect("/")

    return render(request, "reset_password.html", {"teacher_name": adminUser.realname})


# TODO: request 말고, 그냥 adminUser_pk만 받아서 실행하도록. return도 변경.
def send_password_mail(request):
    adminUser_pk = request.session["adminUser_pk"]
    adminUser = AdminUser.objects.get(pk=adminUser_pk)

    while True:
        auth_key = randstr(50)
        if not AdminUser.objects.filter(auth_key=auth_key):
            break

    adminUser.auth_key = auth_key
    adminUser.save()

    mail_title = "컴룸닷컴 비밀번호 재설정"
    mail_args = {"teacher_name": adminUser.realname, "token": adminUser.auth_key}
    mail_context = "컴룸닷컴 비밀번호 재설정"
    mail_html = render_to_string("password_mail.html", mail_args)
    send_mail(
        mail_title,
        mail_context,
        "ssamko@kakao.com",
        [adminUser.email],
        html_message=mail_html,
    )
    message = f"{adminUser.realname} 선생님께서 입력하신 메일({adminUser.email})로\
        비밀번호 재설정 메일을 보내드렸습니다. 8시간 안에 재설정해주세요."
    return render(request, "notice.html", {"message": message})
