# Generated by Django 3.2.9 on 2021-12-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20211208_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
