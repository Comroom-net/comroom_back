from django.contrib import admin
from .models import Timetable

# Register your models here.


class TimetableAdmin(admin.ModelAdmin):

    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d %H:%M")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일시'

    list_display = ('id', '__str__', 'room', 'teacher', 'date_kor')
    list_filter = ('school',)
    search_fields = ['school__name']


admin.site.register(Timetable, TimetableAdmin)
