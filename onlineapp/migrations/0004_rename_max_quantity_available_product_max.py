# Generated by Django 3.2.7 on 2021-10-08 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlineapp', '0003_auto_20211008_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='max_quantity_available',
            new_name='max',
        ),
    ]
