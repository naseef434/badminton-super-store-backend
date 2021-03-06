# Generated by Django 3.2.9 on 2021-11-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20211124_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, to='product.Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(blank=True, to='product.Variant'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='images',
            field=models.ManyToManyField(blank=True, to='product.Image'),
        ),
    ]
