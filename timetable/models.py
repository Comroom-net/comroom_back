from django.db import models


# Create your models here.


class Timetable(models.Model):
    school = models.ForeignKey(
        'school.School', on_delete=models.CASCADE, verbose_name='학교')
    grade = models.IntegerField(verbose_name='학년',
                                choices=(
                                    (1, 1),
                                    (2, 2),
                                    (3, 3),
                                    (4, 4),
                                    (5, 5),
                                    (6, 6)
                                ))
    classNo = models.IntegerField(verbose_name='반')
    date = models.DateField(verbose_name='신청일')
    time = models.IntegerField(verbose_name='예약시간')
    roomNo = models.IntegerField(verbose_name='컴퓨터실번호')
    teacher = models.CharField(max_length=16, verbose_name='선생님')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='예약등록시간')
