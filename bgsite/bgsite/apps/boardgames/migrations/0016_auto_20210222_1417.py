# Generated by Django 3.1.3 on 2021-02-22 11:17

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0015_auto_20210222_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 22, 11, 17, 5, 645412, tzinfo=utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='boardgame',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0, message='Не может быть меньше 0 игр')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Цена для всей корзины'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_product',
            field=models.PositiveIntegerField(default=0, verbose_name='Всего товаров в корзине'),
        ),
    ]
