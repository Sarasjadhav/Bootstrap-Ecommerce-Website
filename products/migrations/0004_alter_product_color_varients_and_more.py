# Generated by Django 5.1.4 on 2025-03-21 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_color_varients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color_varients',
            field=models.ManyToManyField(blank=True, to='products.colorvarient'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size_varients',
            field=models.ManyToManyField(blank=True, to='products.sizevarient'),
        ),
    ]
