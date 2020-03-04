from django.shortcuts import render, redirect
from datetime import datetime, date
from django.http import HttpResponse
from django.utils.safestring import mark_safe
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

    def post(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = {}
        school = School.objects.get(pk=kwargs['pk'])
        roomNo = kwargs['roomNo']
        print(self.request.session['school'])
        print(self.request.session['s_code'])

        # Instantiate calendar class with today's year and date
        cal = TimetableCreate(school=school.name,
                              s_code=school.s_code,
                              roomNo=roomNo)

        # Call the formatmonth method, which returns calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['timetable'] = mark_safe(html_cal)
        # print(context['timetable'])
        return render(request, "timetable.html", context=context)

    def get(self, request, *args, **kwargs):
        return redirect('/')

# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()


def valid_scode(request):
    school = request.GET.get('school')
    s_code = request.GET.get('s_code')

    school_obj = School.objects.get(name__startswith=school, s_code=s_code)

    request.session['school'] = school_obj.name
    request.session['s_code'] = school_obj.s_code
    # if request.method == 'POST':
    #     return render(request, "timetable.html")

    if school_obj:
        print('correct')

        return render(request, "timetable.html", {'school_id': school_obj.id})
        # return redirect('/comroom/'+str(school_obj.id))
    else:
        print('incorrect')

    return redirect('/comroom/1')


class BookingView(FormView):
    template_name = 'booking.html'
    form_class = BookingForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        year = kwargs['year']
        month = kwargs['month']
        day = kwargs['day']
        roomNo = kwargs['roomNo']
        time = kwargs['time']
        return render(request, self.template_name, {'form': form, 'year': year,
                                                    'month': month, 'day': day,
                                                    'roomNo': roomNo, 'time': time})

    def get_context_data(self, **kwargs):
        year = kwargs['year']
