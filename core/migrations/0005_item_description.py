# Generated by Django 3.0 on 2020-08-20 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is a test description fsl lsknfl slknflf slfkn slkfn'),
            preserve_default=False,
        ),
    ]
