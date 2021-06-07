from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar
from .models import Timetable, FixedTimetable
from school.models import School


class TimetableCreate(HTMLCalendar):

    month_name = calendar._localized_month('%m')

    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    cssclasses_weekday_head = cssclasses
    cssclass_month_head = "month"

    calendar.day_abbr = ["월", "화", "수", "목", "금", "토", "일"]
    day_name = ["월", "화", "수", "목", "금"]

    def __init__(self, school_id=None, roomNo=None, year=None, month=None):
        self.year = year
        self.month = month
        self.school = School.objects.get(
            id=school_id)
        self.room = self.school.comroom_set.get(roomNo=roomNo)

        super(TimetableCreate, self).__init__()

    # formats times in a day as buttons
    # filter events by each time
    def formattime(self, day, time, weekday):
        today = int(datetime.now().strftime("%-d"))
        thismonth = int(datetime.now().strftime("%m"))
        date = f'{self.year}-{self.month}-{day}'
        date = parse_date(date)
        d = ''
        is_added = False
        try:
            booked = Timetable.objects.get(
                school=self.school,
                room=self.room,
                date=date,
                time=time
            )
            d += f'<div class="col"><a tabindex="0" role="button" class="btn btn-primary btn-sm booked" data-toggle="popover" data-trigger="focus" title="예약정보" data-content="{booked.grade}-{booked.classNo}. {booked.teacher} 선생님">{time}</a></div>'
        except:
            # 컴실, 요일, 시간이 같은 row가 있는지 filter
            fixedTime = FixedTimetable.objects.filter(
                comroom=self.room,
                fixed_day=weekday,
                fixed_time=time)
            if fixedTime:
                # 있다면 for loop
                for fix in fixedTime:

                    # 현재 row가 해당 기간에 속하는 지 검사
                    if fix.fixed_from <= date and date <= fix.fixed_until:
                        # 속하면 핑크
                        d += f'<div class="col"><a tabindex="0" role="button" class="btn btn-primary btn-sm fixed" data-toggle="popover" data-trigger="focus" title="예약정보" data-content="{fix.fixed_name}">{time}</a></div>'
                        is_added = True
                        break
                    # 속하지 않고, 지난 날이면 회색

                if not is_added:
                    if self.month < thismonth or (day < today and self.month == thismonth):
                        d += f'<div class="col"><a href="#" role="button" class="btn btn-secondary btn-sm disabled">{time}</a></div>'
                    # 둘 다 아니면 파란색
                    else:
                        d += f'<div class="col"><a href="/timetable/{self.school.id}/{self.room.roomNo}/{date}/{time}" role="button" class="btn btn-primary btn-sm">{time}</a></div>'

            else:
                # 없다면 지난 날인지 검사
                if self.month < thismonth or (day < today and self.month == thismonth):
                    d += f'<div class="col"><a href="#" role="button" class="btn btn-secondary btn-sm disabled">{time}</a></div>'
                else:
                    d += f'<div class="col"><a href="/timetable/{self.school.id}/{self.room.roomNo}/{date}/{time}" role="button" class="btn btn-primary btn-sm">{time}</a></div>'

                # else:
                #     if self.month < thismonth or (day < today and self.month == thismonth):
                #         d += f'<div class="col"><a href="#" role="button" class="btn btn-secondary btn-sm disabled">{time}</a></div>'
                #     else:
                #         d += f'<div class="col"><a href="/comroom/{self.school.id}/{self.room.roomNo}/{date}/{time}" role="button" class="btn btn-primary btn-sm">{time}</a></div>'

        return d

    # formats a day as a td
    # filter events by day
    def formatday(self, day, weekday):

        d = ''
        if day != 0:
            date = f'{self.year}-{self.month}-{day}'
            date = parse_date(date)
            for time in range(1, 8):
                d += self.formattime(day, time, weekday)

            return f"<td><span class='date'>{day}</span><div class='row row-cols-4 no-gutter'> {d} </div></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            if not (weekday == 5 or weekday == 6):  # 토, 일 출력x
                week += self.formatday(d, weekday)

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
