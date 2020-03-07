from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar
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

    month_name = calendar._localized_month('%m')

    cssclasses = ["월", "tue", "wed", "thu", "fri", "sat", "sun"]
    cssclasses_weekday_head = cssclasses

    def __init__(self, school_id=None, roomNo=None, year=None, month=None):
        self.year = year
        self.month = month
        self.school = School.objects.get(
            id=school_id)
        self.roomNo = roomNo
        super(TimetableCreate, self).__init__()

    # formats a day as a td
    # filter events by day

    def formatday(self, day):

        d = ''
        if day != 0:
            date = f'{self.year}-{self.month}-{day}'
            date = parse_date(date)
            for time in range(1, 7):
                if Timetable.objects.filter(
                    school=self.school,
                    roomNo=self.roomNo,
                    date=date,
                    time=time
                ):
                    d += f'<div class="col"><a href="#" role="button" class="btn btn-primary btn-sm disabled">{time}</a></div>'
                else:
                    d += f'<div class="col"><a href="/comroom/{self.school.id}/{self.roomNo}/{date}/{time}" role="button" class="btn btn-primary btn-sm">{time}</a></div>'

            return f"<td><span class='date'>{day}</span><div class='row row-cols-3 no-gutter'> {d} </div></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            if not (weekday == 5 or weekday == 6):  # 토, 일 출력x
                week += self.formatday(d)

        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):

        #cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat blue", "sun red"]

        cal = f'<table class="table table-bordered">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        return cal

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s년 %s월' % (theyear, self.month_name[themonth])
        return '<tr><th colspan="5" class="%s">%s</th></tr>' % (
            self.cssclass_month_head, s)

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in range(5))
        return '<tr>%s</tr>' % s
