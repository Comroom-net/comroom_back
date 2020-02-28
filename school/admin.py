from django.contrib import admin
from .models import School, AdminUser
# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    pass


class AdminUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(School, SchoolAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
