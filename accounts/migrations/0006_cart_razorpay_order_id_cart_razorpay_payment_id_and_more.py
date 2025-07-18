# Generated by Django 5.1.4 on 2025-03-28 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
