# Generated by Django 4.0.2 on 2022-03-12 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0010_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offerpercent',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
    ]