# Generated by Django 4.2.4 on 2023-09-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctions_url_alter_auctions_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='url',
            field=models.URLField(default='https://imgur.com/TZjsMoi.jpg/'),
        ),
    ]
