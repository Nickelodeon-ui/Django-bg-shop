# Generated by Django 3.2 on 2021-05-11 21:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0020_auto_20210511_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 11, 21, 43, 16, 341488, tzinfo=utc), verbose_name='Дата добавления'),
        ),
    ]