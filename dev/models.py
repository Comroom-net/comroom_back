from django.db import models


class DevHistory(models.Model):
    title = models.CharField(max_length=64, verbose_name="제목")
    context = models.TextField(verbose_name="내용")
    reg_date = models.DateTimeField(
        verbose_name="등록날짜", auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = "불가 채널"
        verbose_name_plural = "불가 채널"

    def __str__(self):
        return self.ch_name


class DevLike(models.Model):
    devHistory = models.ForeignKey(DevHistory)
    like = models.IntegerField(verbose_name="좋아요")
