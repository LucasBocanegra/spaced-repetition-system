# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('phrase', models.CharField(max_length=800)),
                ('translation', models.CharField(max_length=800)),
                ('level', models.IntegerField(default=0)),
                ('view_data', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('limit_view_cards', models.IntegerField(default=10)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(to='app.Deck'),
        ),
    ]
