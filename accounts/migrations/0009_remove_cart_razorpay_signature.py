# Generated by Django 5.1.4 on 2025-03-29 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_cart_razorpay_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='razorpay_signature',
        ),
    ]
