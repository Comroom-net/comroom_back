# Generated by Django 3.0.3 on 2020-03-16 02:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0009_auto_20200315_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='classNo',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(20)], verbose_name='반'),
        ),
    ]
