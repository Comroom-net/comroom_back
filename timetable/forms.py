from django import forms
from .models import Timetable


class BookingForm(forms.Form):
    grade = forms.IntegerField(
        label='학년',
        widget=forms.Select(
            choices=[
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
                (5, 5),
                (6, 6)
            ]
        )

    )
    classNo = forms.IntegerField(
        label='반',
        error_messages={
            'required': '반을 입력해주세요'
        },

    )
    date = forms.DateField(label='신청일자',
                           widget=forms.HiddenInput())
    time = forms.IntegerField(label='신청시간',
                              widget=forms.HiddenInput())
    roomNo = forms.IntegerField(label='컴퓨터실',
                                widget=forms.HiddenInput())
    school = forms.CharField(label='학교', max_length=128,
    widget=forms.HiddenInput())
    teacher = forms.CharField(
        error_messages={
            'required': '선생님 성함을 입력해주세요'
        },
        label='선생님',
        max_length=64
    )
