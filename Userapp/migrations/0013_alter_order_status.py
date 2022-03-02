# Generated by Django 4.0.2 on 2022-02-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0012_alter_users_propic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('RequestCancellation', 'RequestCancellation'), ('Cancelled', 'Cancelled'), ('Return', 'Return')], default='New', max_length=200, null=True),
        ),
    ]