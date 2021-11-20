# Generated by Django 3.2.7 on 2021-09-11 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_sharing', '0002_auto_20210910_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 11, 14, 51, 22, 478543), verbose_name='End_at'),
        ),
        migrations.AlterField(
            model_name='file',
            name='in_archive',
            field=models.BooleanField(default=False, verbose_name='In_archive'),
        ),
        migrations.AlterField(
            model_name='file',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
