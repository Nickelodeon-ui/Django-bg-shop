# Generated by Django 3.2 on 2021-05-15 00:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0024_auto_20210514_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 15, 0, 34, 8, 691605, tzinfo=utc), verbose_name='Дата добавления'),
        ),
    ]
