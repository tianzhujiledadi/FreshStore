# Generated by Django 2.1.8 on 2019-07-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0006_auto_20190729_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='good_id',
            new_name='goods_id',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='good_name',
            new_name='goods_name',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='good_number',
            new_name='goods_number',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='good_price',
            new_name='goods_price',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='good_store',
            new_name='goods_store',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='good_total',
            new_name='goods_total',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='goods_image',
            field=models.ImageField(default='static/buyer/images/goods001.jpg', upload_to='', verbose_name='商品图片'),
            preserve_default=False,
        ),
    ]
