from django.shortcuts import render
from django.views.generic import FormView
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
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
                password=make_password(form.data.get('user')),
                realname=form.data.get('realname'),
                email=form.data.get('email'),
            )
            adminUser.save()

        return super().form_valid(form)
