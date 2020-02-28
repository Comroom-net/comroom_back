from django import forms
from django.contrib.auth.hashers import check_password
from .models import School, AdminUser


class RegisterForm(forms.Form):
    province = forms.ChoiceField(choices=(
        ('서울특별시교육청', '서울'),
        ('부산광역시교육청', '부산'),
        ('대구광역시교육청', '대구'),
        ('인천광역시교육청', '인천'),
        ('광주광역시교육청', '광주'),
        ('대전광역시교육청', '대전'),
        ('울산광역시교육청', '울산'),
        ('세종특별자치시교육청', '세종'),
        ('경기도교육청', '경기'),
        ('강원도교육청', '강원'),
        ('충청북도교육청', '충북'),
        ('충청남도교육청', '충남'),
        ('전라북도교육청', '전북'),
        ('전라남도교육청', '전남'),
        ('경상북도교육청', '경북'),
        ('경상남도교육청', '경남'),
        ('제주특별자치도교육청', '제주'),
    ), label='교육청',
        error_messages={
        'required': '교육청을 선택해주세요.'
    })
    name = forms.CharField(
        error_messages={
            'required': '학교명을 입력해주세요.'
        },
        max_length=64, label='학교명'
    )
    ea = forms.IntegerField(
        error_messages={
            'required': '교내 컴퓨터실 수를 입력해주세요.'
        },
        label='교내 컴퓨터실 수'
    )
    user = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=64, label='아이디'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, lable='비밀번호'
    )
    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 다시 입력해주세요'
        },
        widget=forms.PasswordInput, lable='비밀번호 확인'
    )
    realname = forms.CharField(
        error_messages={
            'required': '선생님 성함을 입력해주세요.'
        }, max_length=64, label='담당자 이름'
    )
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        label='이메일'
    )

    # 유효성 검사 코드
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')
