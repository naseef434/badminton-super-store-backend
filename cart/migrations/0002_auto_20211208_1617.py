# Generated by Django 3.2.9 on 2021-12-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
