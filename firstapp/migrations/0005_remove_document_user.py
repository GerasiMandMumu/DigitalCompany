# Generated by Django 3.1.2 on 2020-12-07 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_document_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='user',
        ),
    ]
