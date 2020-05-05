from django.db import models


# Create your models here.


class Room(models.Model):
    room_name = models.CharField(max_length=16, verbose_name='방')
    is_available = models.BooleanField(default=True, verbose_name='사용가능여부')

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = '방'
        verbose_name_plural = '방'


class Visitor(models.Model):
    room = models.ForeignKey(
        'Room', on_delete=models.CASCADE, verbose_name='방')
    writer = models.CharField(max_length=16, verbose_name='글쓴이', null=True)
    visitor_image = models.ImageField(
        verbose_name='사진', null=True, blank=True, upload_to='namu/%Y/%m/%d')
    visitor_text = models.TextField(verbose_name='내용')
    visitor_pw = models.CharField(max_length=8, verbose_name='비밀번호')
    is_show = models.BooleanField(default=True, verbose_name='게시')
    reg_date = models.DateTimeField(verbose_name='게시일', auto_now_add=True)

    def __str__(self):
        return f'{self.room} - {self.reg_date}'

    class Meta:
        verbose_name = '방명록'
        verbose_name_plural = '방명록'
