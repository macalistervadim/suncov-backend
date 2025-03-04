# Generated by Django 5.1.6 on 2025-02-20 00:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='title')),
            ],
            options={
                'verbose_name': 'Theme',
                'verbose_name_plural': 'Themes',
            },
        ),
        migrations.CreateModel(
            name='Dictation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dictations', to='dictation.theme', verbose_name='theme')),
            ],
            options={
                'verbose_name': 'Dictation',
                'verbose_name_plural': 'Dictations',
            },
        ),
    ]
