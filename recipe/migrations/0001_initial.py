# Generated by Django 4.0.1 on 2022-03-21 16:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cook_time', models.IntegerField(default=0)),
                ('prep_time', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=800)),
                ('ingredients', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=400), default=list, size=None)),
                ('instructions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=400), default=list, size=None)),
                ('photo_url', models.CharField(default='', max_length=400)),
                ('rating', models.IntegerField(default=0)),
                ('title', models.CharField(default='', max_length=400)),
                ('recipe_url', models.CharField(default='', max_length=400)),
            ],
            options={
                'db_table': 'recipe',
            },
        ),
    ]
