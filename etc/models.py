from django.db import models

# Create your models here.
class Disabled_ch(models.Model):

    ch_name = models.CharField(max_length=64, verbose_name="채널명")
    is_noticed = models.BooleanField(verbose_name="게시여부", default=False)
    reg_date = models.DateTimeField(verbose_name="등록날짜", auto_now=False, auto_now_add=True)
    noticed_date = models.DateTimeField(verbose_name="게시날짜", auto_now=True, auto_now_add=False)


    class Meta:
        verbose_name = "Disabled_ch"
        verbose_name_plural = "Disabled_chs"

    def __str__(self):
        return self.ch_name

    
