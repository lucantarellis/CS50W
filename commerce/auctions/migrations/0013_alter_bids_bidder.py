# Generated by Django 4.2.4 on 2023-09-07 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_auctions_price_remove_bids_actual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]