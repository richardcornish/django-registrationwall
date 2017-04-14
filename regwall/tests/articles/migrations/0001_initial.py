# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-14 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255, verbose_name='Headline')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('body', models.TextField(verbose_name='Body')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Pub date')),
            ],
            options={
                'verbose_name': 'article',
                'ordering': ['-pub_date'],
                'verbose_name_plural': 'articles',
            },
        ),
    ]
