# Generated by Django 4.0.1 on 2022-02-22 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ping', '0007_alter_user_herbs_alter_user_proteins_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]