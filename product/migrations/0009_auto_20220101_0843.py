# Generated by Django 3.2.9 on 2022-01-01 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_variants'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='quantity on hand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(blank=True, to='product.Variant'),
        ),
    ]
