# Generated by Django 4.0.2 on 2022-02-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0018_alter_address_lname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='lname',
            field=models.CharField(max_length=30, null=True),
        ),
    ]