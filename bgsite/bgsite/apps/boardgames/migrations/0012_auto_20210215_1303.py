# Generated by Django 3.1.3 on 2021-02-15 10:03

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boardgames', '0011_auto_20210215_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2021, 2, 15, 10, 3, 1, 435796, tzinfo=utc), verbose_name='Дата добавления'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Количество товара')),
                ('price_for_product', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Цена для товара')),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgames.boardgame', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_product', models.PositiveIntegerField(default=0, verbose_name='Всего различных товаров в корзине')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Цена для всей корзины')),
                ('in_order', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardgames.customer', verbose_name='Владелец')),
                ('products', models.ManyToManyField(blank=True, to='boardgames.CartProduct', verbose_name='Товары в корзине')),
            ],
        ),
    ]
