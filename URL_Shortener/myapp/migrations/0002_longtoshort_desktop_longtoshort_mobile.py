# Generated by Django 4.2.4 on 2023-10-19 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='longtoshort',
            name='desktop',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='longtoshort',
            name='mobile',
            field=models.IntegerField(default=0),
        ),
    ]
