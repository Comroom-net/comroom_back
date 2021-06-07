# Generated by Django 3.0.3 on 2020-02-28 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20200228_0114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminuser',
            options={'verbose_name': '학교관리자', 'verbose_name_plural': '학교관리자'},
        ),
        migrations.AddField(
            model_name='adminuser',
            name='realname',
            field=models.CharField(default='test', max_length=64, verbose_name='이름'),
            preserve_default=False,
        ),
    ]
