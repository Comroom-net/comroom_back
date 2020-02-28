from django.shortcuts import render, redirect
from datetime import datetime, date
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.views.generic import DetailView
from .models import Timetable
from .utils import Calendar, TimetableCreate, TestCalendar
from school.models import School

# Create your views here.


class TimetableView(DetailView):
    model = School
    template_name = "timetable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Instantiate calendar class with today's year and date
        cal = TimetableCreate(school=self.object.name,
                              s_code=self.object.s_code)

        # Call the formatmonth method, which returns calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['timetable'] = mark_safe(html_cal)
        # print(context['timetable'])
        return context


# def get_date(req_day):
#     if req_day:
#         year, month = (int(x) for x in req_day.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()

def valid_scode(request):
    school = request.GET.get('school')
    s_code = request.GET.get('s_code')

    school_obj = School.objects.get(name__startswith=school, s_code=s_code)

    if school_obj:
        print('correct')
        return redirect('/comroom/'+str(school_obj.id))
    else:
        print('incorrect')

    return redirect('/comroom/1')
