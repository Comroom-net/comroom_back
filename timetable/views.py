from django.shortcuts import render, redirect, reverse
from datetime import datetime, date
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView
from .models import Timetable
from .forms import BookingForm
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
        # print(context['timetable'])
        return render(request, "timetable.html", context=context)

    def post(self, request, *args, **kwargs):
        return self.iniTable(request, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.iniTable(request, **kwargs)

# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()


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


# class BookingView(FormView):
#     template_name = 'booking.html'
#     form_class = BookingForm
#     success_url = '/'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         year = kwargs['year']
#         month = kwargs['month']
#         day = kwargs['day']
#         roomNo = kwargs['roomNo']
#         time = kwargs['time']
#         school = School.objects.get(pk=kwargs['pk']).id
#         return render(request, self.template_name, {'form': form, 'year': year,
#                                                     'month': month, 'day': day,
#                                                     'roomNo': roomNo, 'time': time,
#                                                     'school':school})

#     # def get_context_data(self, **kwargs):
#     #     year = kwargs['year']

#     # def post(self, request, *args, **kwargs):
#     #     self.form_valid()

#     def form_valid(self, form):
#         id = form.data.get('school')
#         print('start save')
#         booking = Timetable(
#             school=School.objects.get(pk=id),
#             grade=form.data.get('grade'),
#             classNo=form.data.get('classNo'),
#             date=form.data.get('date'),
#             time=form.data.get('time'),
#             roomNo=form.data.get('roomNo'),
#             teacher=form.data.get('teacher'),
#         )
#         booking.save()
#         print('save')


#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return redirect('/')

def reserving(request, **kwargs):
    template_name = 'booking.html'

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
            roomNo=form.data.get('roomNo'),
            teacher=form.data.get('teacher'),
        )
        booking.save()
        print('save')
        return redirect('/comroom/?school='+school.name+'&s_code='+str(school.s_code))
    if request.method == "GET":
        context = {}
        context['form'] = BookingForm()
        context['date'] = kwargs['date']
        context['roomNo'] = kwargs['roomNo']
        context['time'] = kwargs['time']
        context['school'] = School.objects.get(pk=kwargs['pk']).id

        return render(request, template_name, context)


# class ReservingView(DetailView):
#     template_name = 'booking.html'
#     queryset = School.objects.all()
#     context_object = 'reserve'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['year'] = kwargs['year']
#         context['month'] = kwargs['month']
#         context['day'] = kwargs['day']
#         context['roomNo'] = kwargs['roomNo']
#         context['time'] = kwargs['time']
#         context['school'] = School.objects.get(pk=kwargs['pk']).id
#         context["form"] = BookingForm(self.request)
#         return context
