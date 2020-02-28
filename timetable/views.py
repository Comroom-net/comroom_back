from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import ListView
from django.utils.safestring import mark_safe

from .models import *
from .utils import Calendar

# Create your views here.


class CalendarView(ListView):
    model = Timetable
    template_name = 'timetable.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
