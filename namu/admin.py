from django.contrib import admin

from .models import Room, Visitor

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'is_available')


class VisitorAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d %H:%M")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일시'
    list_display = ('room', 'visitor_text', 'is_show', 'date_kor')


admin.site.register(Room, RoomAdmin)
admin.site.register(Visitor, VisitorAdmin)
