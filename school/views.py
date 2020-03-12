from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.views import View
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.forms import formset_factory
from .forms import RegisterForm, LoginForm, ComroomAdminForm
from .models import School, AdminUser, Notice, Comroom
import random
# Create your views here.


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        with transaction.atomic():

            school = School(
                province=form.data.get('province'),
                name=form.data.get('name'),
                ea=form.data.get('ea'),
                s_code=random.randint(1000, 9999)
            )
            school.save()
            adminUser = AdminUser(
                school=school,
                user=form.data.get('user'),
                password=make_password(form.data.get('password')),
                realname=form.data.get('realname'),
                email=form.data.get('email'),
            )
            self.request.session['username'] = adminUser.realname
            self.request.session['user_id'] = adminUser.user
            adminUser.save()
            for i in range(int(form.data.get('ea'))):
                comroom = Comroom(
                    school=school,
                    roomNo=i+1,
                    name=f"컴{i+1}실"
                )
                comroom.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = form.data.get('user')
        user = AdminUser.objects.get(
            user=user)
        self.request.session['username'] = user.realname
        self.request.session['user_id'] = user.user

        return super().form_valid(form)


def logout(request):
    if 'username' in request.session:
        del(request.session['username'])
        del(request.session['user_id'])

    return redirect('/')


def index(request):
    context = {}

    username = request.session.get('username')
    user_id = request.session.get('user_id')

    # get notice objects
    notices = Notice.objects.filter(isshow=True)
    context['notices'] = notices

    if username:

        school = AdminUser.objects.get(realname=username, user=user_id).school
        context['username'] = username
        context['school'] = school.name
        context['s_code'] = school.s_code
        request.session['school_info'] = school.id

    elif 's_code' in request.session:
        context['s_code'] = request.session['s_code']

    return render(request, 'index.html', context)


class AboutView(TemplateView):
    template_name = "about.html"


class ComroomAdminView(View):
    template_name = 'comroom_admin.html'
    success_url = '/'
    context = {}

    def get(self, request, *args, **kwargs):
        context = self.context
        forms = []
        try:
            school = School.objects.get(id=request.session['school_info'])
        except:
            redirect('/')

        for i in range(school.comroom_set.count()):
            room = school.comroom_set.get(roomNo=i+1)
            # initial form by getting data from DB
            comform = ComroomAdminForm(initial={'room_name': room.name,
                                                'room_caption': room.caption,
                                                })
            #form_name = 'form'+str(i+1)

            forms.append(comform)

        context['forms'] = forms

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.context
        forms = []

        school = School.objects.get(id=request.session['school_info'])

        for i in range(school.comroom_set.count()):

            # bind form with instance
            form = school.comroom_set.get(roomNo=i+1)
            print(form)
            print(request.POST)
            form.name = request.POST['room_name'+str(i+1)]
            form.caption = request.POST['room_caption'+str(i+1)]
            form.save()

        return redirect('/')

    def form_valid(self, form):
        return super().form_valid(form)


def make_room(request):
    schools = School.objects.all()
    for school in schools:
        for room in range(school.ea):
            a = Comroom(school=school,
                        name=f'컴{room+1}실',
                        caption='위치, 이용안내 등',
                        roomNo=room+1)
            a.save()

    return redirect('/')
