from django.contrib import admin
from .models import School, AdminUser, Notice, Comroom
# Register your models here.


class SchoolAdmin(admin.ModelAdmin):

    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일'
    list_display = ('id', 'name', 'province', 'ea', 'date_kor')
    list_filter = ('name', 'province', )
    search_fields = ['school__name']


class AdminUserAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d %H:%M")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일시'
    list_display = ('school', 'realname', 'email', 'date_kor')


class NoticeAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일'
    list_display = ('title', 'isshow', 'date_kor')


class ComroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'roomNo')
    list_filter = ('school',)


admin.site.register(School, SchoolAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Comroom, ComroomAdmin)
