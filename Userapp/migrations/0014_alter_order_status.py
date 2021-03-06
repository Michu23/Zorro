# Generated by Django 4.0.2 on 2022-02-22 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('RequestedCancellation', 'RequestedCancellation'), ('Cancelled', 'Cancelled'), ('Return', 'Return')], default='New', max_length=200, null=True),
        ),
    ]
