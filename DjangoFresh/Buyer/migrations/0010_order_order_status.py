# Generated by Django 2.1.8 on 2019-07-29 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0009_auto_20190729_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(default=1, verbose_name='订单状态'),
        ),
    ]
