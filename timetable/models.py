import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.timezone import now

from school.models import Comroom, School


# Create your models here.


class Timetable(models.Model):
    class Meta:

        verbose_name = '이용시간표'
        verbose_name_plural = '이용시간표'

    def __str__(self):
        return f'{str(self.date)} {str(self.time)}교시'
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
                                ), default=1)
    classNo = models.IntegerField(verbose_name='반',
                                  validators=[
                                      MaxValueValidator(20)
                                  ])
    date = models.DateField(verbose_name='신청일')
    time = models.IntegerField(verbose_name='예약시간',
                               choices=(
                                   (1, 1),
                                   (2, 2),
                                   (3, 3),
                                   (4, 4),
                                   (5, 5),
                                   (6, 6)
                               ))
    # roomNo = models.IntegerField(verbose_name='컴퓨터실번호')
    room = models.ForeignKey('school.Comroom',
                             on_delete=models.CASCADE, verbose_name='교실', null=True)
    teacher = models.CharField(max_length=16, verbose_name='선생님')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='예약등록시간')


class FixedTimetable(models.Model):

    class Meta:

        verbose_name = '고정시간'
        verbose_name_plural = '고정시간'

    next_year = int(datetime.date.today().strftime("%Y"))+1
    til_next_feb = str(next_year)+"0228"
    til_next_feb = datetime.datetime.strptime(til_next_feb, "%Y%m%d")

    comroom = models.ForeignKey(
        Comroom, on_delete=models.CASCADE,
        verbose_name='교실',
        default=1

    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE,
        verbose_name='학교',
        null=True,

    )

    fixed_day = models.IntegerField(
        verbose_name='요일',
        choices=(
            (0, '월'),
            (1, '화'),
            (2, '수'),
            (3, '목'),
            (4, "금"),
        ),
        default=0
    )
    fixed_time = models.IntegerField(
        verbose_name='시간',
        choices=(
            (1, '1교시'),
            (2, '2교시'),
            (3, '3교시'),
            (4, '4교시'),
            (5, '5교시'),
            (6, '6교시')
        ),
        default=1
    )
    fixed_name = models.CharField(
        verbose_name='내용',
        max_length=32
    )
    # default = now
    fixed_from = models.DateField(
        verbose_name='시작일',
        default=now
    )
    # default = next Feb.
    fixed_until = models.DateField(
        verbose_name='종료일',
        default=til_next_feb
    )
    reg_date = models.DateTimeField(
        verbose_name='등록일시',
        auto_now_add=True
    )
