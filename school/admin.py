from django.contrib import admin
from .models import School, AdminUser, Notice, Comroom, IPs
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
    list_display = ('school', 'realname', 'email', 'is_active', 'date_kor')


class NoticeAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.last_update.strftime("%Y-%m-%d")
    date_kor.admin_order_field = 'last_update'
    date_kor.short_description = '수정일'
    list_display = ('title', 'isshow', 'date_kor')


class ComroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'roomNo')
    list_filter = ('school',)


class IPsAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.ip_recent_date.strftime("%Y-%m-%d %H:%m")
    date_kor.admin_order_field = 'ip_recent_date'
    date_kor.short_description = '최근 접속'
    list_display = ('ip', 'date_kor', 'school', 'ip_count', 'ip_first_date')
    list_filter = ('school',)


admin.site.register(School, SchoolAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Comroom, ComroomAdmin)
admin.site.register(IPs, IPsAdmin)
