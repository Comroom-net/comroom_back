from django.contrib import admin
from .models import Timetable

# Register your models here.


class TimetableAdmin(admin.ModelAdmin):
    list_display = ('school', 'grade', 'classNo', 'date',
                    'time', 'roomNo', 'teacher', 'reg_date')


admin.site.register(Timetable, TimetableAdmin)
