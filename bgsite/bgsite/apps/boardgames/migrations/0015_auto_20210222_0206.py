# Generated by Django 3.1.3 on 2021-02-21 23:06

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0014_auto_20210222_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='for_anonymous_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='boardgame',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 23, 6, 0, 228000, tzinfo=utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Цена для всей корзины'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='boardgames.customer', verbose_name='Владелец'),
        ),
    ]
