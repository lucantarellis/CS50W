# Generated by Django 4.2.4 on 2023-09-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_watchlist_delete_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]