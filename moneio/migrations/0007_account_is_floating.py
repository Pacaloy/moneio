# Generated by Django 4.2.3 on 2023-11-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneio', '0006_moneyinout'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_floating',
            field=models.BooleanField(default=False),
        ),
    ]
