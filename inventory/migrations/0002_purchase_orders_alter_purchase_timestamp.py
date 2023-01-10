# Generated by Django 4.1.4 on 2022-12-29 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='orders',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='timestamp',
            field=models.DateTimeField(unique=True),
        ),
    ]
