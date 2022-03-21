# Generated by Django 4.0.1 on 2022-03-21 16:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('herbs', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=3), default=list, null=True, size=None)),
                ('spices', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=3), default=list, null=True, size=None)),
                ('vegetables', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=3), default=list, null=True, size=None)),
                ('proteins', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=3), default=list, null=True, size=None)),
                ('favorite', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, null=True, size=None)),
                ('ban', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, null=True, size=None)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
