from django.contrib import admin
from .models import School, AdminUser
# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'ea', 'reg_date')


class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('school', 'realname', 'email', 'reg_date')


admin.site.register(School, SchoolAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
