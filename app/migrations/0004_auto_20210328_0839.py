# Generated by Django 3.0.2 on 2021-03-28 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_account_twenty_forty_eight_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='twenty_forty_eight_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='twenty_forty_eight_record_points',
            field=models.IntegerField(default=0),
        ),
    ]
