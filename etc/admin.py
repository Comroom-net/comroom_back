from django.contrib import admin
from .models import Disabled_ch, Notice_nocookie, RollFile, HTMLpage

# Register your models here.


class Disabled_chAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.reg_date.strftime("%Y-%m-%d %H:%M")
    date_kor.admin_order_field = 'reg_date'
    date_kor.short_description = '등록일시'
    list_display = ('ch_name', 'is_noticed', 'date_kor')


class Notice_nocookieAdmin(admin.ModelAdmin):
    def date_kor(self, obj):
        return obj.modified_date.strftime("%Y-%m-%d %H:%M")
    date_kor.admin_order_field = 'modified_date'
    date_kor.short_description = '수정일시'
    list_display = ('date_kor',)


class RollFileAdmin(admin.ModelAdmin):
    list_display = ('title',)


class HTMLpageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', )


admin.site.register(Disabled_ch, Disabled_chAdmin)
admin.site.register(Notice_nocookie, Notice_nocookieAdmin)
admin.site.register(RollFile, RollFileAdmin)
admin.site.register(HTMLpage, HTMLpageAdmin)
