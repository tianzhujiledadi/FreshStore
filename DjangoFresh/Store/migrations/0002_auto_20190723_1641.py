# Generated by Django 2.1.2 on 2019-07-23 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='store_descripton',
            new_name='store_description',
        ),
    ]
