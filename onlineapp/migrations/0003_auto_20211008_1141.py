# Generated by Django 3.2.7 on 2021-10-08 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineapp', '0002_shopcart_slide'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='max_quantity_available',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='product',
            name='min',
            field=models.IntegerField(default=1),
        ),
    ]
