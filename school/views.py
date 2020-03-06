from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import School, AdminUser
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

    if username:

        school = AdminUser.objects.get(realname=username, user=user_id).school
        context['username'] = username
        context['school'] = school.name
        context['s_code'] = school.s_code
        context['thisurl'] = 'http://127.0.0.1:8000'
        #context['thisurl'] = 'http://comroom.net:8000'
    return render(request, 'index.html', context)
