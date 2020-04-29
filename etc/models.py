from django.db import models

# Create your models here.


class Disabled_ch(models.Model):

    ch_name = models.CharField(max_length=64, verbose_name="채널명")
    is_noticed = models.BooleanField(verbose_name="게시여부", default=False)
    reg_date = models.DateTimeField(
        verbose_name="등록날짜", auto_now=False, auto_now_add=True)
    noticed_date = models.DateTimeField(
        verbose_name="게시날짜", auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "불가 채널"
        verbose_name_plural = "불가 채널"

    def __str__(self):
        return self.ch_name


class Notice_nocookie(models.Model):

    notice = models.TextField(verbose_name='공지')
    modified_date = models.DateTimeField(
        verbose_name='수정날짜', auto_now=True, auto_now_add=False)

    def __str__(self):
        return "공지"

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'


class RollFile(models.Model):
    title = models.TextField(verbose_name="파일명", default='학교')
    roll_file = models.FileField(upload_to='rolls/%Y/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '명렬표 파일'
        verbose_name_plural = '명렬표 파일'
