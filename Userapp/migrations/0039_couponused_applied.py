# Generated by Django 4.0.2 on 2022-03-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0038_remove_coupondetail_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponused',
            name='applied',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]