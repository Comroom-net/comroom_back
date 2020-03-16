import datetime
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Timetable, FixedTimetable
from school.models import Comroom


# class BookingForm(forms.Form):
#     grade = forms.IntegerField(
#         label='학년',
#         widget=forms.Select(
#             choices=[
#                 (1, 1),
#                 (2, 2),
#                 (3, 3),
#                 (4, 4),
#                 (5, 5),
#                 (6, 6)
#             ]
#         )

#     )
#     classNo = forms.IntegerField(
#         label='반',
#         error_messages={
#             'required': '반을 입력해주세요'
#         },

#     )
#     date = forms.DateField(label='신청일자',
#                            widget=forms.HiddenInput())
#     time = forms.IntegerField(label='신청시간',
#                               widget=forms.HiddenInput())
#     roomNo = forms.IntegerField(label='컴퓨터실',
#                                 widget=forms.HiddenInput())
#     school = forms.CharField(label='학교', max_length=128,
#     widget=forms.HiddenInput())
#     teacher = forms.CharField(
#         error_messages={
#             'required': '선생님 성함을 입력해주세요'
#         },
#         label='선생님',
#         max_length=64
#     )
class BookingForm(forms.ModelForm):
    class Meta:
        model = Timetable
        exclude = ['school', 'date', 'time', 'room', 'reg_date']
        error_messages = {
            'classNo': {
                'required': "반을 입력해주세요.",
                'max_value': "반을 확인해주세요."
            },
            'teacher': {
                'required': "선생님 성함을 입력해주세요."
            },
        }


class FixTimeForm(forms.ModelForm):
    comroom = forms.ModelChoiceField(
        queryset=Comroom.objects.all(),
        label='교실',
        empty_label=None)

    class Meta:
        model = FixedTimetable
        exclude = ['reg_date']
        widgets = {
            'fixed_from': DatePickerInput(format='%Y-%m-%d').start_of('fixed days'),
            'fixed_until': DatePickerInput(format='%Y-%m-%d').end_of('fixed days'),
        }

    def clean_fixed_until(self):
        data = self.cleaned_data['fixed_until']

        # check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('날짜 입력 오류 - 과거를 종료일로 정할 수 없습니다.'))

        # check if a date is on next to ifxed_from.
        if data < self.cleaned_data['fixed_from']:
            raise ValidationError(_('날짜 입력 오류 - 종료일이 시작일보다 빠릅니다.'))

        return data
