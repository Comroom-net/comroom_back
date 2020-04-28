from django.contrib import admin
from .models import Disabled_ch

# Register your models here.


class Disabled_chAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d %H:%M")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일시'
    list_display = ('ch_name', 'is_noticed', 'date_kor')

admin.site.register(Disabled_ch, Disabled_chAdmin)