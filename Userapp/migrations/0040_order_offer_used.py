# Generated by Django 4.0.2 on 2022-03-13 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userapp', '0039_couponused_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='offer_used',
            field=models.CharField(choices=[('None', 'None'), ('ProductOffer', 'ProductOffer'), ('CatogeryOffer', 'CatogeryOffer')], default='None', max_length=50, null=True),
        ),
    ]