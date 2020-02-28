from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Timetable
from school.models import School


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter()
        d = ''
        for event in events_per_day:
            d += f'<li> {event} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)

        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Timetable.objects.filter(
            date__year=self.year, date__month=self.month)

        cal = f'<table class="table table-light">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


class TimetableCreate(HTMLCalendar):
    def __init__(self, school=None, s_code=None):
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.school = School.objects.get(
            name__startswith=school, s_code=s_code)
        super(TimetableCreate, self).__init__()

    # formats a day as a td
    # filter events by day

    def formatday(self, day, events):
        events_per_day = events.filter()
        d = ''
        for event in events_per_day:
            d += f'<li> {event} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)

        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Timetable.objects.filter(
            date__year=self.year, date__month=self.month)

        cal = f'<div class="row mt-5">\
            <div class="col-12 text-center">\
                <h1>{self.school.name} 컴2실</h1></div></div>\n'
        cal += f'<table class="table table-light">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


class TestCalendar(TimetableCreate):

    def __init__(self, school=None, s_code=None):
        self.s_code = s_code
        self.school = school
        super(TestCalendar, self).__init__()
