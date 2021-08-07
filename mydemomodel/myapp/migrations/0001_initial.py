# Generated by Django 2.2.24 on 2021-07-19 03:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('age', models.IntegerField(default=28)),
                ('phone', models.CharField(max_length=16)),
                ('addtime', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]