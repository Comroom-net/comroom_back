# Generated by Django 3.2.4 on 2021-08-08 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_start', models.CharField(max_length=10, verbose_name='1교시 시작시간')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school', verbose_name='학교')),
            ],
        ),
    ]
