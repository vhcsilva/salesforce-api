# Generated by Django 2.2.1 on 2021-04-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210128_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderheader',
            name='obs',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
