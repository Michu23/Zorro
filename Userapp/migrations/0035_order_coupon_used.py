# Generated by Django 4.0.2 on 2022-03-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0034_rename_use_count_coupondetail_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_used',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]