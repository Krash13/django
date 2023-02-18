# Generated by Django 4.0.4 on 2023-02-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reagents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('quantity', models.FloatField(default=0)),
                ('units', models.IntegerField(choices=[(1, 'mg'), (2, 'g'), (3, 'kg'), (4, 'ml'), (5, 'l')], verbose_name='Единицы измерения')),
                ('place', models.CharField(default='', max_length=500)),
                ('last_update_date', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
            ],
            options={
                'verbose_name': 'Реагенты',
                'verbose_name_plural': 'Реагенты',
            },
        ),
    ]