# Generated by Django 3.1.2 on 2020-12-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0009_auto_20201207_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='Адрес',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='Информация',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='image',
            name='Название',
            field=models.CharField(max_length=255),
        ),
    ]