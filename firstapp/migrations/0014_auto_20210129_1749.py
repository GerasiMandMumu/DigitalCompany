# Generated by Django 3.1.2 on 2021-01-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0013_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('question', models.TextField()),
                ('answers', models.TextField()),
                ('right_answer', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
