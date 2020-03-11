from django.contrib import admin
from .models import School, AdminUser, Notice
# Register your models here.


class SchoolAdmin(admin.ModelAdmin):

    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일'
    list_display = ('name', 'province', 'ea', 'date_kor')


class AdminUserAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일'
    list_display = ('school', 'realname', 'email', 'date_kor')


class NoticeAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일'
    list_display = ('title', 'isshow', 'date_kor')


admin.site.register(School, SchoolAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(Notice, NoticeAdmin)
