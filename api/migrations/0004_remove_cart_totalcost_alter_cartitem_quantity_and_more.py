# Generated by Django 5.0.7 on 2024-07-14 12:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='totalCost',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]