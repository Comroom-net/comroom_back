# Generated by Django 3.0.3 on 2020-03-11 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_auto_20200311_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comroom',
            options={'verbose_name_plural': '컴퓨터실 정보'},
        ),
        migrations.RenameField(
            model_name='comroom',
            old_name='classNo',
            new_name='roomNo',
        ),
    ]
