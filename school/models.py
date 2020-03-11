from django.db import models


# Create your models here.
province_list = [
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
]


class School(models.Model):
    province = models.CharField(max_length=32, verbose_name='교육청',
                                choices=province_list)
    name = models.CharField(max_length=64, verbose_name='학교명')
    s_code = models.IntegerField(verbose_name='학교코드')
    ea = models.IntegerField(verbose_name='컴퓨터실 수')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:

        verbose_name = '학교'
        verbose_name_plural = '학교'

    def __str__(self):
        return str(self.name)+f'({str(self.province)})'


class AdminUser(models.Model):
    school = models.ForeignKey(
        'School', on_delete=models.CASCADE, verbose_name='학교')
    user = models.CharField(max_length=64, verbose_name='아이디')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    realname = models.CharField(max_length=64, verbose_name='이름')
    email = models.EmailField(verbose_name='이메일')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:
        verbose_name = '학교관리자'
        verbose_name_plural = '학교관리자'

    def __str__(self):
        return str(self.school)+f'_{str(self.realname)}'


class Notice(models.Model):

    title = models.CharField(max_length=128, verbose_name='제목')
    context = models.TextField(verbose_name='내용')
    isshow = models.BooleanField(verbose_name='게시여부')
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'

    def __str__(self):
        return self.title
