# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numb', models.CharField(max_length=20)),
                ('netbar_name', models.CharField(max_length=20)),
                ('usable', models.CharField(max_length=4)),
                ('jlzt', models.CharField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Netbar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numb', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('boss_name', models.CharField(max_length=20)),
                ('jlzt', models.CharField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=40)),
                ('vipid', models.CharField(max_length=20)),
                ('cardno', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('sex', models.CharField(max_length=4)),
                ('jlzt', models.CharField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_comp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=40)),
                ('comp_numb', models.CharField(max_length=20)),
                ('kssj', models.DateTimeField()),
                ('jssj', models.DateTimeField()),
                ('zje', models.FloatField(max_length=10)),
                ('xfje', models.FloatField(max_length=10)),
                ('jlzt', models.CharField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
