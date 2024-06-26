# Generated by Django 4.2.4 on 2023-09-04 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_categories_alter_bids_last'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='url',
            field=models.URLField(default='https://imgur.com/TZjsMoi.jpg'),
        ),
        migrations.AlterField(
            model_name='auctions',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
