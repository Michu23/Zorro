# Generated by Django 4.0.2 on 2022-03-12 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0012_product_offerbuycount'),
    ]

    operations = [
        migrations.AddField(
            model_name='catogery',
            name='catoffer',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='catogery',
            name='catpercent',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
    ]
