# Generated by Django 3.0.2 on 2021-03-25 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210325_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='twenty_forty_eight_field',
            field=models.TextField(default=''),
        ),
    ]
