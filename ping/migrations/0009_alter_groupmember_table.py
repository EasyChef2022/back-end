# Generated by Django 4.0.1 on 2022-02-22 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ping', '0008_delete_user'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='groupmember',
            table='group_member',
        ),
    ]
