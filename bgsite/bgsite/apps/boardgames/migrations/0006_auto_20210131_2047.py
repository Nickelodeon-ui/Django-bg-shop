# Generated by Django 3.1.3 on 2021-01-31 17:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0005_auto_20210127_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2021, 1, 31, 17, 47, 50, 252520, tzinfo=utc), verbose_name='Дата добавления'),
        ),
    ]
