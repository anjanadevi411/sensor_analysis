# Generated by Django 4.0.1 on 2022-01-14 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ph',
            new_name='Phsensor',
        ),
        migrations.RenameModel(
            old_name='Tm',
            new_name='Temp',
        ),
    ]
