from datetime import datetime, date
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, CreateView
from .models import Timetable, FixedTimetable
from .forms import BookingForm, FixTimeForm
from .utils import TimetableCreate
from .decorators import method_dectect
from school.models import School


# Create your views here.


class TimetableView(DetailView):
    model = School
    template_name = "timetable.html"

    def iniTable(self, request, roomNo=1, date=None):
        context = {}
        try:
            school_id = self.request.session['school']
        except:
            return redirect('/')

        school = School.objects.get(pk=school_id)
        ea = school.ea
        roomNo = roomNo
        date = date.split('-')
        year = int(date[0])
        month = int(date[1])

        # Instantiate calendar class with today's year and date
        cal = TimetableCreate(school_id=school.id,
                              roomNo=roomNo,
                              year=year,
                              month=month)

        # Call the formatmonth method, which returns calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['timetable'] = mark_safe(html_cal)
        context['school'] = school.name
        context['roomNo'] = roomNo
        context['year'] = year
        context['month'] = month
        context['ea'] = range(1, ea+1)
        context['comroom'] = school.comroom_set.get(roomNo=roomNo)
        context['roomset'] = school.comroom_set.all()
        # print(context['timetable'])
        return render(request, "timetable.html", context=context)

    def post(self, request, *args, **kwargs):
        return self.iniTable(request, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.iniTable(request, **kwargs)


def valid_scode(request):
    school = request.GET.get('school')
    s_code = request.GET.get('s_code')

    school_obj = School.objects.get(name__startswith=school, s_code=s_code)

    date = datetime.now().strftime("%Y-%m")

    context = {}

    if school_obj:
        print('correct')
        request.session['school'] = school_obj.id
        request.session['s_code'] = school_obj.s_code
        context['school_id'] = school_obj.id
        context['date'] = date
        context['roomNo'] = 1
        return render(request, "timetable.html", context=context)

    else:
        print('incorrect')

    return redirect('/comroom/1')


def reserving(request, **kwargs):
    template_name = 'booking.html'
    context = {}

    if request.method == 'POST':

        form = BookingForm(request.POST)

        school = School.objects.get(pk=kwargs['pk'])
        print('start save')
        booking = Timetable(
            school=school,
            grade=form.data.get('grade'),
            classNo=form.data.get('classNo'),
            date=form.data.get('date'),
            time=form.data.get('time'),
            teacher=form.data.get('teacher'),
            room=school.comroom_set.get(roomNo=form.data.get('roomNo'))
        )
        booking.save()
        print('save')
        return redirect('/comroom/?school='+school.name+'&s_code='+str(school.s_code))
    if request.method == "GET":
        context = {}
        school = School.objects.get(pk=kwargs['pk'])
        context['form'] = BookingForm()
        context['date'] = kwargs['date']
        context['roomNo'] = kwargs['roomNo']
        context['time'] = kwargs['time']
        context['school'] = school.name
        context['room_name'] = school.comroom_set.get(
            roomNo=kwargs['roomNo']).name

        return render(request, template_name, context)

    return render(request, template_name, context)


class BookTime(FormView):
    template_name = 'booking.html'
    form_class = BookingForm
    url_date = datetime.now().strftime("%Y-%m")
    success_url = '/comroom/1/'+url_date
    school_id = 2
    date = '2020-01-08'
    time = 1
    roomNo = 1

    # def get(self, request, *args, **kwargs):
    #     self.school_id = kwargs['pk']
    #     self.date = kwargs['date']
    #     self.time = kwargs['time']
    #     self.roomNo = kwargs['roomNo']
    #     return render(request, self.template_name, {'form': BookingForm()})

    def get(self, request, *args, **kwargs):
        school_id = self.request.session['school']
        school = School.objects.get(id=school_id)
        comroom = school.comroom_set.get(roomNo=kwargs['roomNo'])
        self.room = comroom.name
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        school = School.objects.get(pk=self.kwargs['pk'])
        booking = Timetable(
            school=school,
            grade=form.cleaned_data['grade'],
            classNo=form.cleaned_data['classNo'],
            teacher=form.cleaned_data['teacher'],
            date=datetime.strptime(self.kwargs['date'], "%Y-%m-%d"),
            time=self.kwargs['time'],
            room=school.comroom_set.get(roomNo=self.kwargs['roomNo'])
        )
        booking.save()
        return super().form_valid(form)


# Timetable model에 room field추가에 따른 기존 data에 foreign key assign
def assign_room(request):
    timetables = Timetable.objects.all()
    for timetable in timetables:
        timetable.room = timetable.school.comroom_set.get(
            roomNo=timetable.roomNo)
        timetable.save()

    return redirect('/')


class FixCreateView(CreateView):
    template_name = 'fixTime.html'
    form_class = FixTimeForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        context = {}
        school_id = self.request.session['school']
        school = School.objects.get(id=school_id)
        comroom = school.comroom_set.filter(school=school)
        form = FixTimeForm()
        form.fields['comroom'].queryset = comroom
        context['form'] = form
        return render(request, self.template_name, context)
