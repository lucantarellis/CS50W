# Generated by Django 4.2.4 on 2023-10-01 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_alter_auctions_starting_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
