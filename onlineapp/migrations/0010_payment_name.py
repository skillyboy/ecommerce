# Generated by Django 4.0.5 on 2022-09-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineapp', '0009_shopcart_basket_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(default=1, max_length=36),
            preserve_default=False,
        ),
    ]
