# Generated by Django 4.0.2 on 2022-03-10 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0037_coupondetail_applied'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupondetail',
            name='applied',
        ),
    ]
