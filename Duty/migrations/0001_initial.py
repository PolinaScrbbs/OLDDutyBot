# Generated by Django 5.0.4 on 2024-04-20 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, unique=True, verbose_name='ФИО')),
                ('group', models.CharField(blank=True, max_length=10, verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Человек',
                'verbose_name_plural': 'Люди',
            },
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата дежурства')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='duties', to='Duty.people', verbose_name='Человек')),
            ],
            options={
                'verbose_name': 'Дежурство',
                'verbose_name_plural': 'Дежурства',
            },
        ),
    ]
