# Generated by Django 4.0.2 on 2022-03-09 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0033_coupondetail_usecoupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupondetail',
            old_name='use_count',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='coupondetail',
            old_name='created_date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='coupondetail',
            old_name='exp_date',
            new_name='expdate',
        ),
        migrations.RenameField(
            model_name='coupondetail',
            old_name='total_lessed_money',
            new_name='loss',
        ),
        migrations.RenameField(
            model_name='coupondetail',
            old_name='offer_percentage',
            new_name='percentage',
        ),
        migrations.RenameField(
            model_name='usecoupon',
            old_name='lessed_money',
            new_name='loss',
        ),
        migrations.RenameField(
            model_name='usecoupon',
            old_name='fororder',
            new_name='order',
        ),
    ]
