# Generated by Django 2.1.8 on 2019-05-17 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_auto_20190517_1212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='img',
            new_name='picture',
        ),
    ]
